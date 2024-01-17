#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!pip install openpyxl


# In[2]:


#!pip install dash-bootstrap-components


# In[3]:


from dash import Dash, dcc, html
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
from gensim.models.phrases import Phrases, Phraser
from dash import Dash, html, dcc
import numpy as np
import pandas as pd
import cufflinks as cf
from plotly.subplots import make_subplots
from plotly import graph_objects as go
#get_ipython().run_line_magic('matplotlib', 'inline')
from plotly.offline import init_notebook_mode
init_notebook_mode(connected=True)
cf.go_offline()

# WORD2VEC
# common
# languages

# tách thành từ riêng biệt


# In[4]:


# base='caphe_sen_pie.xlsx'

#df.time=df.apply(lambda x: datetime.strftime(x['time'],'%Y-%m') ,axis=1)
# data = np.random.randint(0,2,size=len(df)+1)
# data_1 = np.random.randint(0,2,size=len(df)+1)
# data_2 = np.random.randint(0,2,size=len(df)+1)

# #df = pd.DataFrame(data, columns=['Service'])
# df['Service'] = pd.Series(data)
# df['Price'] = pd.Series(data_1)
# df['Quality'] = pd.Series(data_2)
# # df.to_excel('test/caphe_sen_pie.xlsx',engine='xlsxwriter')
# data_others=[]
# for i in range(0,len(df)):
#     if int('1') in [df['Service'][i],df['Price'][i],df['Quality'][i]]:
#         data_others.append(0)
#     else:
#         data_others.append(1)
# df['Others']= data_others
# df


# # Plot Word2vec

# In[5]:


# tách thành từ riêng biệt


def plot_Wordcloud(base):
    df = pd.read_excel(base, engine='openpyxl')
    sent = [row.split() for row in df['comment_1'].astype(str)]

    # nhận diện từ phổ biến
    phrases = Phrases(sent, min_count=30, progress_per=10000)

    # cut down memory consumption
    bigram = Phraser(phrases)
    sentences = bigram[sent]
    from collections import defaultdict
    word_freq = defaultdict(int)
    for sent in sentences:
        for i in sent:
            word_freq[i] += 1

    freq = ''
    for word in df['comment_1'].dropna():
        words = word.split()
        for i in range(len(words)):
            words[i] = words[i].lower()
        freq = freq + ' '.join(words)+' '

    # tao word cloud

    # img=np.array(Image.open("C:/Users/LVC/OneDrive - Industrial University of HoChiMinh City/Pictures/DAK.jpg"))
    img = np.array(Image.open(
        "D:/Code/Stech/AMR-Stech-main/AMRFLASK/1024_768_not_included.png"))
    wordcloud = WordCloud(max_words=1500,
                          background_color='white',
                          width=664, height=669,
                          max_font_size=25,  # random_state=38,
                          collocations=False,
                          mask=img).generate(freq)

    image_colors = ImageColorGenerator(img)
    wordcloud.recolor(color_func=image_colors)

    word_cloud_img = np.array(wordcloud)
    len(word_cloud_img)
    dak_word_img = wordcloud.to_image()
    # dak_word_img.save("dak_word.jpg")
    return dak_word_img


# # Plot_Pie

# In[6]:


def data_pie(base):
    df = pd.read_excel(base, engine='openpyxl')
    # Test
    #df['Source'][0:50] = pd.Series(["Voz new" for x in range(len(df))])[0:50]
    #df['Source'][:] = pd.Series(["Lazada" for x in range(len(df))])[:]
    #df['Source'][100:200] = pd.Series(["Tiki" for x in range(len(df))])[100:200]
    data_others = []
    for i in range(0, len(df)):
        if int('1') in [df['Service'][i], df['Price'][i], df['Quality'][i]]:
            data_others.append(0)
        else:
            data_others.append(1)
    df['Others'] = data_others
    df

    def choose_columns(df):
        dic = []
        for i in range(4, len(df.columns)):
            dic.append(df.columns[i])
        fruit_dictionary = dict.fromkeys(dic, "sum")
        return fruit_dictionary

    df_catogary = df
    df_catogary = df_catogary[['predict', 'Source',
                               'Service', 'Price', 'Quality', 'Others']]
    df_catogary = pd.get_dummies(df_catogary, columns=['Source', 'predict'])
    df_catogary = df_catogary.groupby(
        ['Service', 'Price', 'Quality', 'Others']).agg(choose_columns(df_catogary))

    df_Service = pd.concat([df_catogary[4:]])
    df_Price = pd.concat([df_catogary[2:4], df_catogary[6:8]])
    df_Quality = pd.concat(
        [df_catogary[1:2], df_catogary[3:4], df_catogary[5:6], df_catogary[7:8]])
    df_Others = df_catogary[0:1]

    df_Service_Sum = pd.DataFrame(df_Service.sum(axis=0), columns=['Service'])
    df_Price_Sum = pd.DataFrame(df_Price.sum(axis=0), columns=['Price'])
    df_Quality_Sum = pd.DataFrame(df_Quality.sum(axis=0), columns=['Quality'])
    df_Others_Sum = pd.DataFrame(df_Others.sum(axis=0), columns=['Others'])

    df_Pie = pd.concat([df_Service_Sum, df_Price_Sum,
                       df_Quality_Sum, df_Others_Sum], axis=1)
    df_Pie = df_Pie.transpose()
    df_Pie['Sum_Source'] = df_Pie.iloc[:, 0:-3].sum(axis=1)
    df_Pie['Sum_Predict'] = df_Pie.iloc[:, -4:-1].sum(axis=1)

    custom = []

    for col in df_Pie.columns:
        if ('Source_' in col or 'predict_' in col):
            custom.append(col)

    return df_Pie, custom


# # Plot Sentiment

# In[7]:


def pie_4_func(df_Pie, custom):
    fig = make_subplots(
        rows=1, cols=1,
        specs=[[{'type': 'pie'}]]
        #subplot_titles=("Table", "Pie Chart")
    )

    fig.add_trace(go.Pie(labels=['Service', 'Price', 'Quality', 'Others'], values=df_Pie['Sum_Predict'], pull=[0.1, 0, 0, 0],
                         customdata=np.transpose([df_Pie[custom[0]], df_Pie[custom[1]], df_Pie[custom[2]], df_Pie[custom[3]],
                                                  df_Pie[custom[4]], df_Pie[custom[5]], df_Pie[custom[6]]]),
                         hovertemplate="<br> Catogary:%{label} <br>" +
                         df_Pie.columns[0] + ": %{customdata[0][0]} comments <br>" +
                         df_Pie.columns[1] + ": %{customdata[0][1]} comments <br>" +
                         df_Pie.columns[2] + ": %{customdata[0][2]} comments <br>" +
                         df_Pie.columns[3] + ": %{customdata[0][3]} comments <br>" +
                         df_Pie.columns[4] + ": %{customdata[0][4]} comments <br>" +
                         df_Pie.columns[5] + ": %{customdata[0][5]} comments <br>" +
                         df_Pie.columns[6] +
                         ": %{customdata[0][6]} comments <br>",


                         textposition='inside', textinfo='percent+label', name='Pie_Chart',
                         insidetextfont=dict(size=30),
                         ))

    fig.update_xaxes(
        tickfont=dict(size=15, family='monospace', color='#B8B8B8'),
        tickmode='array',
        ticklen=6,
        showline=False,
        showgrid=True,
        gridcolor='#595959',
        ticks='outside')

    fig.update_xaxes(
        showspikes=True,
        spikesnap="cursor",
        spikemode="across"
    )
    fig.update_yaxes(
        showspikes=True,
        spikesnap='cursor',
        spikemode="across"
    )
    fig.update_yaxes(
        tickfont=dict(size=15, family='monospace', color='#B8B8B8'),
        tickmode='array',
        showline=False,
        #ticksuffix = '$',
        showgrid=True,
        gridcolor='#595959',
        ticks='outside')
    fig.update_layout(
        width=1150,
        height=1000,
        autosize=True,
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4),
        font_family='monospace',
        font=dict(color="black"),

        template="plotly_white",
    )
    return fig


def pie_3_func(df_Pie, custom):
    fig = make_subplots(
        rows=1, cols=1,
        specs=[[{'type': 'pie'}]]
        #subplot_titles=("Table", "Pie Chart")
    )

    fig.add_trace(go.Pie(labels=['Service', 'Price', 'Quality', 'Others'], values=df_Pie['Sum_Predict'], pull=[0.1, 0, 0],
                         customdata=np.transpose([df_Pie[custom[0]], df_Pie[custom[1]], df_Pie[custom[2]], df_Pie[custom[3]],
                                                  df_Pie[custom[4]], df_Pie[custom[5]]]),
                         hovertemplate="<br> Catogary:%{label} <br>" +
                         df_Pie.columns[0] + ": %{customdata[0][0]} comments <br>" +
                         df_Pie.columns[1] + ": %{customdata[0][1]} comments <br>" +
                         df_Pie.columns[2] + ": %{customdata[0][2]} comments <br>" +
                         df_Pie.columns[3] + ": %{customdata[0][3]} comments <br>" +
                         df_Pie.columns[4] + ": %{customdata[0][4]} comments <br>" +
                         # df_Pie.columns[6] + ": %{customdata[0][6]} comments <br>"
                         df_Pie.columns[5] + \
                         ": %{customdata[0][5]} comments <br>",


                         textposition='inside', textinfo='percent+label', name='Pie_Chart',
                         insidetextfont=dict(size=30),
                         ))

    fig.update_xaxes(
        tickfont=dict(size=15, family='monospace', color='#B8B8B8'),
        tickmode='array',
        ticklen=6,
        showline=False,
        showgrid=True,
        gridcolor='#595959',
        ticks='outside')

    fig.update_xaxes(
        showspikes=True,
        spikesnap="cursor",
        spikemode="across"
    )
    fig.update_yaxes(
        showspikes=True,
        spikesnap='cursor',
        spikemode="across"
    )
    fig.update_yaxes(
        tickfont=dict(size=15, family='monospace', color='#B8B8B8'),
        tickmode='array',
        showline=False,
        #ticksuffix = '$',
        showgrid=True,
        gridcolor='#595959',
        ticks='outside')
    fig.update_layout(
        width=1150,
        height=1000,
        autosize=True,
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4),
        font_family='monospace',
        font=dict(color="black"),

        template="plotly_white",
    )
    return fig


def pie_2_func(df_Pie, custom):
    fig = make_subplots(
        rows=1, cols=1,
        specs=[[{'type': 'pie'}]]
        #subplot_titles=("Table", "Pie Chart")
    )

    fig.add_trace(go.Pie(labels=['Service', 'Price', 'Quality', 'Others'], values=df_Pie['Sum_Predict'], pull=[0.1, 0, 0, 0],
                         customdata=np.transpose([df_Pie[custom[0]], df_Pie[custom[1]], df_Pie[custom[2]], df_Pie[custom[3]],
                                                  df_Pie[custom[4]]]),
                         hovertemplate="<br> Catogary:%{label} <br>" +
                         df_Pie.columns[0] + ": %{customdata[0][0]} comments <br>" +
                         df_Pie.columns[1] + ": %{customdata[0][1]} comments <br>" +
                         df_Pie.columns[2] + ": %{customdata[0][2]} comments <br>" +
                         df_Pie.columns[3] + ": %{customdata[0][3]} comments <br>" +
                         # df_Pie.columns[5] + ": %{customdata[0][5]} comments <br>"+
                         # df_Pie.columns[6] + ": %{customdata[0][6]} comments <br>"
                         df_Pie.columns[4] + \
                         ": %{customdata[0][4]} comments <br>",


                         textposition='inside', textinfo='percent+label', name='Pie_Chart',
                         insidetextfont=dict(size=30),
                         ))

    fig.update_xaxes(
        tickfont=dict(size=15, family='monospace', color='#B8B8B8'),
        tickmode='array',
        ticklen=6,
        showline=False,
        showgrid=True,
        gridcolor='#595959',
        ticks='outside')

    fig.update_xaxes(
        showspikes=True,
        spikesnap="cursor",
        spikemode="across"
    )
    fig.update_yaxes(
        showspikes=True,
        spikesnap='cursor',
        spikemode="across"
    )
    fig.update_yaxes(
        tickfont=dict(size=15, family='monospace', color='#B8B8B8'),
        tickmode='array',
        showline=False,
        #ticksuffix = '$',
        showgrid=True,
        gridcolor='#595959',
        ticks='outside')
    fig.update_layout(
        width=1150,
        height=1000,
        autosize=True,
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4),
        font_family='monospace',
        font=dict(color="black"),

        template="plotly_white",
    )
    return fig


def pie_1_func(df_Pie, custom):
    fig = make_subplots(
        rows=1, cols=1,
        specs=[[{'type': 'pie'}]]
        #subplot_titles=("Table", "Pie Chart")
    )

    fig.add_trace(go.Pie(labels=['Service', 'Price', 'Quality', 'Others'], values=df_Pie['Sum_Predict'], pull=[0.1, 0, 0, 0],
                         customdata=np.transpose([df_Pie[custom[0]], df_Pie[custom[1]], df_Pie[custom[2]], df_Pie[custom[3]]
                                                  ]),
                         hovertemplate="<br> Catogary:%{label} <br>" +
                         df_Pie.columns[0] + ": %{customdata[0][0]} comments <br>" +
                         df_Pie.columns[1] + ": %{customdata[0][1]} comments <br>" +
                         df_Pie.columns[2] + ": %{customdata[0][2]} comments <br>" +
                         # df_Pie.columns[4] + ": %{customdata[0][4]} comments <br>"+
                         # df_Pie.columns[5] + ": %{customdata[0][5]} comments <br>"+
                         # df_Pie.columns[6] + ": %{customdata[0][6]} comments <br>"
                         df_Pie.columns[3] + \
                         ": %{customdata[0][3]} comments <br>",


                         textposition='inside', textinfo='percent+label', name='Pie_Chart',
                         insidetextfont=dict(size=30),
                         ))

    fig.update_xaxes(
        tickfont=dict(size=15, family='monospace', color='#B8B8B8'),
        tickmode='array',
        ticklen=6,
        showline=False,
        showgrid=True,
        gridcolor='#595959',
        ticks='outside')

    fig.update_xaxes(
        showspikes=True,
        spikesnap="cursor",
        spikemode="across"
    )
    fig.update_yaxes(
        showspikes=True,
        spikesnap='cursor',
        spikemode="across"
    )
    fig.update_yaxes(
        tickfont=dict(size=15, family='monospace', color='#B8B8B8'),
        tickmode='array',
        showline=False,
        #ticksuffix = '$',
        showgrid=True,
        gridcolor='#595959',
        ticks='outside')
    fig.update_layout(
        width=1150,
        height=1000,
        autosize=True,
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4),
        font_family='monospace',
        font=dict(color="black"),

        template="plotly_white",
    )
    return fig


# In[8]:


# base = 'caphe_sen_pie.xlsx'
base = 'D:\Code\Stech\AMR-Stech-main\AMRFLASK\caphe_sen_pie.xlsx'


def piechart(base):
    df_Pie, custom = data_pie(base)

    len_col = len(custom) - 3

    if len_col == 4:
        fig = pie_4_func(df_Pie, custom)
    elif len_col == 3:
        fig = pie_3_func(df_Pie, custom)
    elif len_col == 2:
        fig = pie_2_func(df_Pie, custom)
    else:
        fig = pie_1_func(df_Pie, custom)
    return fig


# In[9]:


# In[10]:

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.config['suppress_callback_exceptions'] = True

theme = {
    'dark': True,
    'detail': '#2d3038',  # Background-card
    'primary': '#007439',  # Green
    'secondary': '#FFD15F',  # Accent
}

app.layout = html.Div(children=[

    html.H1("This is top 10 frequency words in your data and pie chart of Sentiment",
            style={'text-align': 'center'}),


    html.Img(id='image_1', src=plot_Wordcloud(base),
             style={'display': 'inline-block', 'margin-left': '30px'},
             title='WORDCLOUD'),


    dcc.Graph(id='exam_graph_1', figure=piechart(base),
              style={  # 'margin-left':'15px',
        'width': '80vh', 'height': '80vh',
        'display': 'inline-block'}
    ),


])


# In[ ]:


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.config['suppress_callback_exceptions'] = True

theme = {
    'dark': True,
    'detail': '#2d3038',  # Background-card
    'primary': '#007439',  # Green
    'secondary': '#FFD15F',  # Accent
}

app.layout = html.Div(children=[

    html.H1("This is top 10 frequency words in your data and pie chart of Sentiment",
            style={'text-align': 'center'}),

    html.Img(id='image_1', src=plot_Wordcloud(base),
             style={'display': 'inline-block', 'margin-left': '30px'},
             title='WORDCLOUD'),

    dcc.Graph(id='exam_graph_1', figure=piechart(base),
              style={  # 'margin-left':'15px',
                  'width': '80vh', 'height': '80vh',
                  'display': 'inline-block'}
              ),

])

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False, port='1000')


# In[ ]:
