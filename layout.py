from dash import dcc, html
import pandas as pd
import numpy as np
from plotly import graph_objects as go
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from gensim.models.phrases import Phrases, Phraser
import multiprocessing
from gensim.models import Word2Vec
from collections import defaultdict
from Draw_Dashboard_PievsWordcloud import piechart, plot_Wordcloud
#from line_chart_v1 import linechart
from Draw_Dashboard_LinevsBar import line_chart
#from pie_chart import piechart, draw_figr
from PIL import Image


word_labels = []
test = ''


def home_layout():
    return html.Div(children=[
        #html.H1(children="Home Page"),
        html.H2(children='''
                    Dash: A web application framework for your data.
                ''', style={'text-align': 'center', 'color': '#5F9EA0'}),
        dcc.Link('Home', href="/dash"),
        html.Br(),
        dcc.Link('Line Chart', href="/dash/linechart"),
        html.Br(),
        dcc.Link('Pie Chart', href="/dash/piechart"),
        html.Br(),
    ])


def piechart_layout(base):
    return html.Div(children=[
        html.H1(children='Sentiment Analysis', style={'text-align': 'center',
                                                      'color': '#484848'
                                                      }),
        dcc.Link('LineChart', href="/dash/linechart", refresh=True),
        html.Br(),
        dcc.Link('Chart3D', href="/dash/chart3D", refresh=True),

        html.H2(children='''
                This is top 10 frequency words in your data and pie chart of Sentiment
            ''', style={'text-align': 'center', 'color': '#5F9EA0'}),

        html.Img(id='image_1', src=plot_Wordcloud(base),
                 style={'display': 'inline-block', 'margin-left': '30px'},
                 title='WORDCLOUD'),

        dcc.Graph(id='exam_graph_1', figure=piechart(base),
                  style={  # 'margin-left':'15px',
                      'width': '80vh', 'height': '80vh',
                      'display': 'inline-block'}
                  ),
        # dcc.Graph(
        #     id='example-graph',
        #     figure=piechart(base), style={'height': '80vh'}
        # ),
    ])


def linechart_layout(base):
    return html.Div(children=[
        html.H1(children='Sentiment Analysis', style={'text-align': 'center',
                                                      'color': '#484848'
                                                      }),
        dcc.Link('PieChart', href="/dash/piechart", refresh=True),
        html.Br(),
        dcc.Link('Chart3D', href="/dash/chart3D", refresh=True),

        html.H2(children='''
        Visualization data for Sentiment
    ''', style={'text-align': 'center', 'color': '#5F9EA0'}),

        dcc.Graph(
            id='example-graph',
            figure=line_chart(base), style={'height': '80vh'}
        )
    ])


def w2v_model(base):
    df = pd.read_excel(base, engine='openpyxl')
    sent = [row.split() for row in df['comment_1'].astype(str)]
    vocab = []
    for s in sent:
        for w in s:
            vocab.append(w)
    phrases = Phrases(sent, min_count=30, progress_per=10000)
    bigram = Phraser(phrases)
    sentences = bigram[sent]
    word_freq = defaultdict(int)
    #print ('word_freg: ', word_freq)
    for sent in sentences:
        for i in sent:
            word_freq[i] += 1

    cores = multiprocessing.cpu_count()
    model = Word2Vec(sg=1,
                     seed=42,
                     vector_size=300,
                     window=7,
                     min_count=3,
                     workers=cores
                     )
    model.build_vocab(sentences, progress_per=10000)

    model.train(sentences, total_examples=model.corpus_count,
                epochs=30, report_delay=1)

    return model, vocab


def tsne_scatter_plot_combine(word, model, vocab):
    """ Plot in seaborn the results from the t-SNE dimensionality reduction algorithm of the vectors of a query word,
    its list of most similar words, and a list of words.
    """
    # print ('model corpus: ', model.corpus)

    # pyLogo = Image.open('D:/PCCC-QuanLyDuAn/AMRFLASK/1024_768_not_included.png')
    pyLogo = Image.open(
        "D:\\Code\\Stech\\AMR-Stech-main\\AMRFLASK\\1024_768_not_included.png")
    try:
        global test
        test = 'Yes'
        arrays = np.empty((0, 300), dtype='f')
        global word_labels
        word_labels = [word]
        # print ('1')
        # print (word_labels)
        # print ('word_labels: ', word_labels)
        color_list = ['yellow']
        type_list = ['main_word']

        # add button dropdown
        buttons = [{'label': '2D plot', 'method': 'update',
                    'args': [{'visible': [False, False, False, True, True, True]},
                             {'title': 'in 2D'}]},
                   {'label': '3D plot', 'method': 'update',
                    'args': [{'visible': [True, True, True, False, False, False]},
                             {'title': 'in 3D'}]}]

        # adds the vector of the query word
        arrays = np.append(arrays, model.wv.__getitem__([word]), axis=0)
        # print ('2')
        # print (model.wv.__getitem__([word]))
        # gets list of most similar words
        close_words = model.wv.most_similar([word])

        # adds the vector for each of the closest words to the array
        for wrd_score in close_words:
            wrd_vector = model.wv.__getitem__([wrd_score[0]])
            word_labels.append(wrd_score[0])
            # print ('2: ', word_labels)
            color_list.append('green')
            type_list.append('close_word')
            arrays = np.append(arrays, wrd_vector, axis=0)

        # gets list of most similar words
        notclose_words = model.wv.most_similar(negative=[word])

        # adds the vector for each of the closest words to the array
        for wrd_score in notclose_words:
            wrd_vector = model.wv.__getitem__([wrd_score[0]])
            word_labels.append(wrd_score[0])
            # print ('3: ', word_labels)
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
        # print ('word_labels: ', word_labels)
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
                          xaxis=dict(showgrid=True, zeroline=False,
                                     visible=False),
                          yaxis=dict(showgrid=True, zeroline=False,
                                     visible=False),
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

    except:
        test = 'No'
        fig = go.Figure()

        # Constants
        img_width = 1024
        img_height = 768
        scale_factor = 1

        # Add invisible scatter trace.
        # This trace is added to help the autoresize logic work.
        fig.add_trace(
            go.Scatter(
                x=[0, img_width * scale_factor],
                y=[0, img_height * scale_factor],
                mode="markers",
                marker_opacity=0
            )
        )

        # Configure axes
        fig.update_xaxes(
            visible=False,
            range=[0, img_width * scale_factor]
        )

        fig.update_yaxes(
            visible=False,
            range=[0, img_height * scale_factor],
            # the scaleanchor attribute ensures that the aspect ratio stays constant
            scaleanchor="x"
        )

        # Add image
        fig.add_layout_image(
            dict(
                x=0,
                sizex=img_width * scale_factor,
                y=img_height * scale_factor,
                sizey=img_height * scale_factor,
                xref="x",
                yref="y",
                # opacity=1.0,
                layer="below",
                sizing="stretch",
                source=pyLogo)
        )

        # Configure other layout
        fig.update_layout(
            width=img_width * scale_factor,
            height=img_height * scale_factor,
            margin={"l": 0, "r": 0, "t": 0, "b": 0},
        )
    return fig

#text = input('text: ')
#fig = tsne_scatter_plot_combine(text, base)
# fig.show()
# def graph_3D_layout(word, base):
#     return html.Div(children=[
#
#     html.Div([
#
#         "Input: ",
#         dcc.Input(id='my-input', style={'marginRight': '10px', 'color': 'yellow',
#                                         'text-align': 'center',
#                                         'background-color': 'black',
#                                         'border-color': 'white'},
#                   type='text'),
#     ]),
#     html.Br(),
#
#     dcc.Graph(
#         id='example-graph',
#         figure = tsne_scatter_plot_combine(word, base)
#     ),
#
# ])
