from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from collections import defaultdict
import multiprocessing
from time import time

import numpy as np
# WORD2VEC
# common
import pandas as pd
import seaborn as sns
from gensim.models import Word2Vec
from gensim.models.phrases import Phrases, Phraser
from plotly import graph_objects as go

base = 'data/caphe_sen.xlsx'
#base = 'data/caphe_sen.xlsx'
df = pd.read_excel(base, engine='openpyxl')
#df.time=df.apply(lambda x: datetime.strftime(x['time'],'%Y-%m') ,axis=1)
sent = [row.split() for row in df['comment_1'].astype(str)]
phrases = Phrases(sent, min_count=30, progress_per=10000)
bigram = Phraser(phrases)
sentences = bigram[sent]
word_freq = defaultdict(int)
for sent in sentences:
    for i in sent:
        word_freq[i] += 1
# len(word_freq)


# WORD2VEC
W2V_SIZE = 300
W2V_WINDOW = 7  # max distance bt the current and predicted
W2V_EPOCH = 32
W2V_MIN_COUNT = 3  # Ignore word frequence < n
TRAIN_SIZE = 0.9
SG = 1  # 1
HS = 1  # 1: softmax is used for model, 0: negative sample used
NEGATIVE = 5  # (5:20: noise words) 0 no-used
CBOW_MEAN = 1  # 0: sum , 1: mean
ALPHA = 0.001  # learning rate
MIN_ALPHA = 0.01
SEED = 42  # random
SAMPLE = 1e-3  # 0->1e-5
COMPUTE_LOSS = True  # loss value retrieved using
# KERAS
SEQUENCE_LENGTH = 50
EPOCHS = 20
BATCH_SIZE = 32


cores = multiprocessing.cpu_count()


w2v_model = Word2Vec(sg=SG,
                     #hs =HS,
                     #negative = NEGATIVE,
                     # max_vocab_size=None,
                     # cbow_mean=CBOW_MEAN,
                     # alpha=ALPHA,
                     # min_alpha=MIN_ALPHA,
                     seed=SEED,
                     # sample=SAMPLE,
                     # compute_loss=COMPUTE_LOSS,
                     size=W2V_SIZE,
                     window=W2V_WINDOW,
                     min_count=W2V_MIN_COUNT,
                     workers=cores
                     )


t = time()
w2v_model.build_vocab(sentences, progress_per=10000)
print('Time to build vocab: {} mins'.format(round((time() - t) / 60, 2)))
w2v_model.train(sentences, total_examples=w2v_model.corpus_count,
                epochs=30, report_delay=1)
print('Time to train the model: {} mins'.format(round((time() - t) / 60, 2)))


sns.set_style("darkgrid")


def tsne_scatter_plot_combine(model, word):
    """ Plot in seaborn the results from the t-SNE dimensionality reduction algorithm of the vectors of a query word,
    its list of most similar words, and a list of words.
    """
    arrays = np.empty((0, 300), dtype='f')
    word_labels = [word]
    color_list = ['yellow']
    type_list = ['main_word']

    # add button dropdown
    buttons = [{'label': '3D plot', 'method': 'update',
                'args': [{'visible': [True, True, True, False, False, False]},
                         {'title': 'in 3D'}]},
               {'label': '2D plot', 'method': 'update',
                'args': [{'visible': [False, False, False, True, True, True]},
                         {'title': 'in 2D'}]}]

    # adds the vector of the query word
    arrays = np.append(arrays, model.wv.__getitem__([word]), axis=0)

    # gets list of most similar words
    close_words = model.wv.most_similar([word])

    # adds the vector for each of the closest words to the array
    for wrd_score in close_words:
        wrd_vector = model.wv.__getitem__([wrd_score[0]])
        word_labels.append(wrd_score[0])
        color_list.append('green')
        type_list.append('close_word')
        arrays = np.append(arrays, wrd_vector, axis=0)

    # gets list of most similar words
    notclose_words = model.wv.most_similar(negative=[word])

    # adds the vector for each of the closest words to the array
    for wrd_score in notclose_words:
        wrd_vector = model.wv.__getitem__([wrd_score[0]])
        word_labels.append(wrd_score[0])
        color_list.append('red')
        type_list.append('argon_word')
        arrays = np.append(arrays, wrd_vector, axis=0)

    # Reduces the dimensionality from 300 to 50 dimensions with PCA
    reduc = PCA(n_components=10).fit_transform(arrays)

    # Finds t-SNE coordinates for 2,3 dimensions
    np.set_printoptions(suppress=True)

    Y = TSNE(n_components=3, random_state=0,
             perplexity=15).fit_transform(reduc)
    # for 2D
    Y_2D = TSNE(n_components=2, random_state=0,
                perplexity=15).fit_transform(reduc)

    # Sets everything up to plot
    df_2w = pd.DataFrame({'x': [x for x in Y[:, 0]],
                          'y': [y for y in Y[:, 1]],
                          'z': [z for z in Y[:, 2]],
                          'words': word_labels,
                          'color': color_list,
                          'type': type_list})

    df_2w_2D = pd.DataFrame({'x': [x for x in Y_2D[:, 0]],
                             'y': [y for y in Y_2D[:, 1]],
                             'words': word_labels,
                             'color': color_list,
                             'type': type_list})

    # make dataFrame of type
    df_cl = df_2w[1:11]
    df_ar = df_2w[11:]

    df_cl_2D = df_2w_2D[1:11]
    df_ar_2D = df_2w_2D[11:]

    # DRAW 3D
    fig = go.Figure()

    fig.add_trace(go.Scatter3d(
        x=df_2w['x'][0:1],
        y=df_2w['y'][0:1],  # <-- Put your data instead
        z=df_2w['z'][0:1],  # <-- Put your data instead
        text=df_2w['words'][0:1],
        name='main word',
        mode='markers+text',
        hovertemplate="<br>".join(["word: %{text}"]),
        marker={
            'size': 10,
            'opacity': 0.8,
            'color': df_2w.color,
        }
    ))

    fig.add_trace(go.Scatter3d(
        x=df_cl['x'],
        y=df_cl['y'],  # <-- Put your data instead
        z=df_cl['z'],  # <-- Put your data instead
        text=df_cl['words'],
        name='close of main word',
        mode='markers+text',
        hovertemplate="<br>".join(["word: %{text}"]),
        marker={
            'size': 10,
            'opacity': 0.8,
            'color': df_cl['color'],
        }
    ))

    fig.add_trace(go.Scatter3d(
        x=df_ar['x'],
        y=df_ar['y'],  # <-- Put your data instead
        z=df_ar['z'],  # <-- Put your data instead
        text=df_ar['words'],
        name='argon of main word',
        mode='markers+text',
        hovertemplate="<br>".join(["word: %{text}"]),

        marker={
            'size': 10,
            'opacity': 0.8,
            'color': df_ar['color'],
        }
    ))

    # DRAW 2D

    fig.add_trace(go.Scatter(
        x=df_2w_2D['x'][0:1],
        y=df_2w_2D['y'][0:1],  # <-- Put your data instead
        # z=df_2w['z'],  # <-- Put your data instead
        text=df_2w_2D['words'][0:1],
        name='main word',
        mode='markers+text',
        hovertemplate="<br>".join(["word: %{text}"]),
        textposition="top center",
        marker={
            'size': 20,
            'opacity': 1,
            'color': df_2w_2D.color[0:1],
        }
    ))

    fig.add_trace(go.Scatter(
        x=df_cl_2D['x'],
        y=df_cl_2D['y'],  # <-- Put your data instead
        # z=df_cl['z'],  # <-- Put your data instead
        text=df_cl_2D['words'],
        name='close of main word',
        mode='markers+text',
        hovertemplate="<br>".join(["word: %{text}"]),
        textposition="top center",
        marker={
            'size': 20,
            'opacity': 1,
            'color': df_cl_2D['color'],
        }
    ))

    fig.add_trace(go.Scatter(
        x=df_ar_2D['x'],
        y=df_ar_2D['y'],  # <-- Put your data instead
        # z=df_ar['z'],  # <-- Put your data instead
        text=df_ar_2D['words'],
        name='argon of main word',
        mode='markers+text',
        hovertemplate="<br>".join(["word: %{text}"]),
        textposition="top center",
        marker={
            'size': 20,
            'opacity': 1,
            'color': df_ar_2D['color'],
        }
    ))

    fig.update_xaxes(
        showspikes=True,
        spikesnap="cursor",
        spikemode="across")
    fig.update_yaxes(
        showspikes=True,
        spikesnap='cursor',
        spikemode="across"
    )
    # Configure the layout.
    fig.update_layout(width=1800,
                      height=900,
                      showlegend=True,
                      updatemenus=[dict(type='dropdown',
                                        x=1.0,
                                        y=1.108,
                                        showactive=True,
                                        active=1,
                                        buttons=buttons),
                                   ],
                      xaxis=dict(showgrid=True, zeroline=False, visible=False),
                      yaxis=dict(showgrid=True, zeroline=False, visible=False),
                      # margin={'l': 0, 'r': 0, 'b': 0, 't': 0},
                      margin=dict(l=65, r=50, b=65, t=90),
                      template="plotly_white"
                      )
    fig.data[5].visible = False
    fig.data[4].visible = False
    fig.data[3].visible = False
    fig.data[2].visible = True
    fig.data[1].visible = True
    fig.data[0].visible = True

    return fig
