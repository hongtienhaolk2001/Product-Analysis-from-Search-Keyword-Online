import pandas as pd
import numpy as np
import warnings

import plotly.graph_objects as go
from plotly.subplots import make_subplots

warnings.filterwarnings('ignore')

base = 'caphe_sen.xlsx'

def data_line(base):
    df_test = pd.read_excel(base, engine='openpyxl')
    # df.time=df.apply(lambda x: datetime.strftime(x['time'],'%Y-%m') ,axis=1)
    # df_test['Source'].replace('vozforum','Tiki',inplace=True)
    df_sen = df_test
    df_bar = df_test
    # Test
    #df_sen['Source'][0:50] = pd.Series(["Voz new" for x in range(len(df_test))])[0:50]
    #df_sen['Source'][50:100] = pd.Series(["Lazada" for x in range(len(df_test))])[50:100]
    #df_sen['Source'][100:200] = pd.Series(["Tiki" for x in range(len(df_test))])[100:200]
    # select
    START_DATE = "2018-11-15"  # start date for historical data
    # df_sen=df_test
    # df_3.time=df_3.apply(lambda x: datetime.strftime(x['time'],'%Y-%m') ,axis=1)
    df_sen = df_sen[['time', 'predict', 'Source']]
    df_sen = pd.get_dummies(df_sen, columns=['Source'])

    def choose_columns(df):
        dic = []
        if df.columns[1] == 'predict':
            for i in range(2, len(df.columns)):
                dic.append(df.columns[i])
            fruit_dictionary = dict.fromkeys(dic, "sum")
        else:
            for i in range(1, len(df.columns)):
                dic.append(df.columns[i])
            fruit_dictionary = dict.fromkeys(dic, "sum")
        return fruit_dictionary

    df_sen = df_sen.groupby(['time', 'predict']).agg(
        choose_columns(df_sen)).reset_index()

    df_sen['sum_pre'] = df_sen.sum(axis=1, numeric_only=True)

    df_sen.set_index('time', inplace=True)

    df_sen = df_sen[df_sen.index > START_DATE]

    df_bar = df_bar[['time', 'predict']]
    df_bar = pd.get_dummies(df_bar, columns=['predict'])
    df_bar = df_bar.groupby(['time']).agg(choose_columns(df_bar))
    df_bar['sum'] = df_bar.sum(axis=1, numeric_only=True)
    # df_bar.set_index('time',inplace=True)

    df_bar = df_bar[df_bar.index > START_DATE]

    # get Hover and custom
    def get_el(df_sen):
        test = df_sen.columns.values
        hover = []
        custom = []
        for col in test:
            if 'Source' in col:
                custom.append(col)
                hov = col.split('_')[1]
                hover.append(hov)
        return hover, custom
    df_neg = df_sen[df_sen.predict == 'negative']
    df_pos = df_sen[df_sen.predict == 'positive']
    df_neu = df_sen[df_sen.predict == 'neutral']
    hover, custom = get_el(df_sen)
    return df_bar, df_neg, df_pos, df_neu, hover, custom
# In[8]:


def all_4_func(df_bar, df_neg, df_pos, df_neu, hover, custom):
    START_DATE = "2015-11-15"  # start date for historical data
    RSI_TIME_WINDOW = 7  # number of days

    # plot
    fig = make_subplots(rows=3,
                        cols=1,
                        shared_xaxes=True,
                        specs=[[{"rowspan": 2}], [{"rowspan": 1}], [{}]]
                        )
    date_buttons = [
        {'step': "all", 'label': "All time"},
        {'count':  1, 'step': "year", 'stepmode': "backward", 'label': "Last Year"},
        {'count':  1, 'step': "year", 'stepmode': "todate", 'label': "Current Year"},
        {'count':  6, 'step': "month", 'stepmode': "backward", 'label': "Last 6 Months"},
        {'count':  1, 'step': "month", 'stepmode': "todate", 'label': "Current Month"},
        {'count':  7, 'step': "day", 'stepmode': "todate", 'label': "Current Week"},
        {'count':  4, 'step': "day", 'stepmode': "backward", 'label': "Last 4 days"},
        {'count':  1, 'step': "day", 'stepmode': "backward", 'label': "Today"},
    ]

    fig.add_trace(go.Scatter(x=df_neu.index, y=df_neu['sum_pre'],
                             customdata=np.transpose([df_neu[custom[0]], df_neu[custom[1]],
                                                      df_neu[custom[2]], df_neu[custom[3]]]),

                             hovertemplate="<br>time: %{x}<br>" +
                             "Total comments: %{y}<br>" +
                             hover[0]+": %{customdata[0]}<br>" +
                             hover[1]+": %{customdata[1]}<br>" +
                             hover[2]+": %{customdata[2]}<br>" +
                             hover[3]+": %{customdata[3]}<br>",
                             name='neutral_comment',
                             showlegend=False
                             ),
                  row=1,
                  col=1)

    fig.add_trace(
        go.Scatter(x=df_neg.index, y=df_neg['sum_pre'],
                   customdata=np.transpose([df_neg[custom[0]], df_neg[custom[1]],
                                            df_neg[custom[2]], df_neg[custom[3]]]),
                   hovertemplate="<br>time: %{x}<br>" +
                   "Total comments: %{y}<br>" +
                   hover[0]+": %{customdata[0]}<br>" +
                   hover[1]+": %{customdata[1]}<br>" +
                   hover[2]+": %{customdata[2]}<br>" +
                   hover[3]+": %{customdata[3]}<br>",
                   name='negative_comment',
                   showlegend=False,
                   ),
        row=1,
        col=1)
    fig.add_trace(go.Scatter(x=df_pos.index, y=df_pos['sum_pre'],
                             customdata=np.transpose([df_pos[custom[0]], df_pos[custom[1]],
                                                      df_pos[custom[2]], df_pos[custom[3]]]),
                             hovertemplate="<br>time: %{x}<br>" +
                             "num_comments: %{y}<br>" +
                             hover[0]+": %{customdata[0]}<br>" +
                             hover[1]+": %{customdata[1]}<br>" +
                             hover[2]+": %{customdata[2]}<br>" +
                             hover[3]+": %{customdata[3]}<br>",
                             name='positive_comment',
                             showlegend=False
                             ),
                  row=1,
                  col=1)
    fig.add_trace(
        go.Bar(x=df_bar.index,
               y=df_bar["sum"],
               customdata=np.transpose([df_bar['predict_negative'],
                                        df_bar['predict_positive'], df_bar['predict_neutral']]),
               hovertemplate="<br>time: %{x}<br>" +
               "Total comments: %{y}<br>" +
               "Negative: %{customdata[0]}<br>" +
               "Positive: %{customdata[1]}<br>" +
               "Neutral: %{customdata[2]}",
               name='comment_in_day',
               showlegend=False,
               marker_color='blueviolet'),
        row=3,
        col=1)

    fig.update_xaxes(
        tickfont=dict(size=15, family='monospace', color='#B8B8B8'),
        tickmode='array',
        ticklen=6,
        showline=False,
        showgrid=False,
        gridcolor='#595959',
        ticks='outside')
    fig.update_layout(
        spikedistance=100,
        xaxis_rangeslider_visible=False,
        hoverdistance=1000)
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
        showline=True,
        #ticksuffix = '$',
        showgrid=False,
        gridcolor='#595959',
        ticks='outside')
    fig.update_layout(
        width=1900,
        height=1000,
        font_family='monospace',
        xaxis=dict(rangeselector=dict(buttons=date_buttons)),
        updatemenus=[dict(type='dropdown',
                          x=1.0,
                          y=1.108,
                          showactive=True,
                          active=2,
                          )],
        title=dict(text='<b>Sentiment Analysis<b>',
                   font=dict(color='#FFFFFF', size=22),
                   x=0.50),
        font=dict(color="orangered"),
        annotations=[
            dict(text="<b>Choose Cryptocurrency: <b>",
                 font=dict(size=20, color="#ffffff"),
                 showarrow=False,
                 x=1.02,
                 y=1.20,
                 xref='paper', yref="paper",
                 align="left"),
            dict(text="<b>Candlestick Chart <b>",
                 font=dict(size=20,  color="#ffffff"),
                 showarrow=False,
                 x=1.02,
                 y=1.20,
                 xref='paper', yref="paper",
                 align="left"),
            # dict( text = "<b>Price Chart<b>",
            #      font = dict(size = 20,  color = "#ffffff"),
            #      showarrow=False,
            #      x = 0.82,
            #     y = 0.285,
            #     xref = 'paper', yref = "paper",
            #     align = "left"),
            dict(text="<b>Volume Traded<b>",
                 font=dict(size=20,  color="#ffffff"),
                 showarrow=False,
                 x=0.14,
                 y=-0.53,
                 xref='paper', yref="paper",
                 align="left"),
            dict(text="<b>Relative Strength Index (RSI)<b>",
                 font=dict(size=20,  color="#ffffff"),
                 showarrow=False,
                 x=0.94,
                 y=-0.53,
                 xref='paper', yref="paper",
                 align="left")
        ],
        template="plotly_white",
        yaxis_showgrid=False,
        xaxis_showgrid=False
    )
    fig.layout["xaxis3"]["rangeslider"]["borderwidth"] = 4
    fig.layout["xaxis3"]["rangeslider"]["bordercolor"] = "blueviolet"
    fig.layout["yaxis3"]["ticksuffix"] = ""
    return fig


# In[9]:


def all_3_func(df_bar, df_neg, df_pos, df_neu, hover, custom):
    START_DATE = "2015-11-15"  # start date for historical data
    RSI_TIME_WINDOW = 7  # number of days

    # plot
    fig = make_subplots(rows=3,
                        cols=1,
                        shared_xaxes=True,
                        specs=[[{"rowspan": 2}], [{"rowspan": 1}], [{}]]
                        )
    date_buttons = [
        {'step': "all", 'label': "All time"},
        {'count': 1, 'step': "year", 'stepmode': "backward", 'label': "Last Year"},
        {'count': 1, 'step': "year", 'stepmode': "todate", 'label': "Current Year"},
        {'count': 6, 'step': "month", 'stepmode': "backward", 'label': "Last 6 Months"},
        {'count': 1, 'step': "month", 'stepmode': "todate", 'label': "Current Month"},
        {'count': 7, 'step': "day", 'stepmode': "todate", 'label': "Current Week"},
        {'count': 4, 'step': "day", 'stepmode': "backward", 'label': "Last 4 days"},
        {'count': 1, 'step': "day", 'stepmode': "backward", 'label': "Today"}, ]

    fig.add_trace(go.Scatter(x=df_neu.index, y=df_neu['sum_pre'],
                             customdata=np.transpose([df_neu[custom[0]], df_neu[custom[1]],
                                                      df_neu[custom[2]]]),

                             hovertemplate="<br>time: %{x}<br>" +
                             "Total comments: %{y}<br>" +
                             hover[0] + ": %{customdata[0]}<br>" +
                             hover[1] + ": %{customdata[1]}<br>" +
                             # hover[3]+": %{customdata[3]}<br>"
                             hover[2] + ": %{customdata[2]}<br>",
                             name='neutral_comment',
                             showlegend=False
                             ),
                  row=1,
                  col=1)

    fig.add_trace(
        go.Scatter(x=df_neg.index, y=df_neg['sum_pre'],
                   customdata=np.transpose([df_neg[custom[0]], df_neg[custom[1]],
                                            df_neg[custom[2]]]),

                   hovertemplate="<br>time: %{x}<br>" +
                   "Total comments: %{y}<br>" +
                   hover[0] + ": %{customdata[0]}<br>" +
                   hover[1] + ": %{customdata[1]}<br>" +
                   # hover[3]+": %{customdata[3]}<br>"
                   hover[2] + ": %{customdata[2]}<br>",
                   name='neutral_comment',
                   showlegend=False
                   ),
        row=1,
        col=1)
    fig.add_trace(go.Scatter(x=df_pos.index, y=df_pos['sum_pre'],
                             customdata=np.transpose([df_pos[custom[0]], df_pos[custom[1]],
                                                      df_pos[custom[2]]]),

                             hovertemplate="<br>time: %{x}<br>" +
                             "Total comments: %{y}<br>" +
                             hover[0] + ": %{customdata[0]}<br>" +
                             hover[1] + ": %{customdata[1]}<br>" +
                             # hover[3]+": %{customdata[3]}<br>"
                             hover[2] + ": %{customdata[2]}<br>",
                             name='neutral_comment',
                             showlegend=False
                             ),
                  row=1,
                  col=1)

    fig.add_trace(
        go.Bar(x=df_bar.index,
               y=df_bar["sum"],
               customdata=np.transpose([df_bar['predict_negative'],
                                        df_bar['predict_positive'], df_bar['predict_neutral']]),
               hovertemplate="<br>time: %{x}<br>" +
               "Total comments: %{y}<br>" +
               "Negative: %{customdata[0]}<br>" +
               "Positive: %{customdata[1]}<br>" +
               "Neutral: %{customdata[2]}",
               name='comment_in_day',
               showlegend=False,
               marker_color='blueviolet'),
        row=3,
        col=1)

    fig.update_xaxes(
        tickfont=dict(size=15, family='monospace', color='#B8B8B8'),
        tickmode='array',
        ticklen=6,
        showline=False,
        showgrid=False,
        gridcolor='#595959',
        ticks='outside')
    fig.update_layout(
        spikedistance=100,
        xaxis_rangeslider_visible=False,
        hoverdistance=1000)
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
        showline=True,
        # ticksuffix = '$',
        showgrid=False,
        gridcolor='#595959',
        ticks='outside')
    fig.update_layout(
        width=1900,
        height=1000,
        font_family='monospace',
        xaxis=dict(rangeselector=dict(buttons=date_buttons)),
        updatemenus=[dict(type='dropdown',
                          x=1.0,
                          y=1.108,
                          showactive=True,
                          active=2,
                          )],
        title=dict(text='<b>Sentiment Analysis<b>',
                   font=dict(color='#FFFFFF', size=22),
                   x=0.50),
        font=dict(color="orangered"),
        annotations=[
            dict(text="<b>Choose Cryptocurrency: <b>",
                 font=dict(size=20, color="#ffffff"),
                 showarrow=False,
                 x=1.02,
                 y=1.20,
                 xref='paper', yref="paper",
                 align="left"),
            dict(text="<b>Candlestick Chart <b>",
                 font=dict(size=20, color="#ffffff"),
                 showarrow=False,
                 x=1.02,
                 y=1.20,
                 xref='paper', yref="paper",
                 align="left"),
            # dict( text = "<b>Price Chart<b>",
            #      font = dict(size = 20,  color = "#ffffff"),
            #      showarrow=False,
            #      x = 0.82,
            #     y = 0.285,
            #     xref = 'paper', yref = "paper",
            #     align = "left"),
            dict(text="<b>Volume Traded<b>",
                 font=dict(size=20, color="#ffffff"),
                 showarrow=False,
                 x=0.14,
                 y=-0.53,
                 xref='paper', yref="paper",
                 align="left"),
            dict(text="<b>Relative Strength Index (RSI)<b>",
                 font=dict(size=20, color="#ffffff"),
                 showarrow=False,
                 x=0.94,
                 y=-0.53,
                 xref='paper', yref="paper",
                 align="left")
        ],
        template="plotly_white",
        yaxis_showgrid=False,
        xaxis_showgrid=False
    )
    fig.layout["xaxis3"]["rangeslider"]["borderwidth"] = 4
    fig.layout["xaxis3"]["rangeslider"]["bordercolor"] = "blueviolet"
    fig.layout["yaxis3"]["ticksuffix"] = ""
    return fig


# In[10]:


def all_2_func(df_bar, df_neg, df_pos, df_neu, hover, custom):
    START_DATE = "2015-11-15"  # start date for historical data
    RSI_TIME_WINDOW = 7  # number of days

    # plot
    fig = make_subplots(rows=3,
                        cols=1,
                        shared_xaxes=True,
                        specs=[[{"rowspan": 2}], [{"rowspan": 1}], [{}]]

                        )
    date_buttons = [
        {'step': "all", 'label': "All time"},
        {'count':  1, 'step': "year", 'stepmode': "backward", 'label': "Last Year"},
        {'count':  1, 'step': "year", 'stepmode': "todate", 'label': "Current Year"},
        {'count':  6, 'step': "month", 'stepmode': "backward", 'label': "Last 6 Months"},
        {'count':  1, 'step': "month", 'stepmode': "todate", 'label': "Current Month"},
        {'count':  7, 'step': "day", 'stepmode': "todate", 'label': "Current Week"},
        {'count':  4, 'step': "day", 'stepmode': "backward", 'label': "Last 4 days"},
        {'count':  1, 'step': "day", 'stepmode': "backward", 'label': "Today"},
    ]

    fig.add_trace(go.Scatter(x=df_neu.index, y=df_neu['sum_pre'],
                             customdata=np.transpose([df_neu[custom[0]], df_neu[custom[1]],
                                                      ]),

                             hovertemplate="<br>time: %{x}<br>" +
                             "Total comments: %{y}<br>" +
                             hover[0]+": %{customdata[0]}<br>" +
                             # hover[2]+": %{customdata[2]}<br>"
                             # hover[3]+": %{customdata[3]}<br>"
                             hover[1]+": %{customdata[1]}<br>",
                             name='neutral_comment',
                             #open  = df['open'],
                             #high  = df['high'],
                             #low   = df['low'],
                             #close = df['close'],
                             showlegend=False
                             ),
                  row=1,
                  col=1)

    fig.add_trace(
        go.Scatter(x=df_neg.index, y=df_neg['sum_pre'],
                   customdata=np.transpose([df_neg[custom[0]], df_neg[custom[1]],
                                            ]),

                   hovertemplate="<br>time: %{x}<br>" +
                   "Total comments: %{y}<br>" +
                   hover[0]+": %{customdata[0]}<br>" +
                   # hover[2]+": %{customdata[2]}<br>"
                   # hover[3]+": %{customdata[3]}<br>"
                   hover[1]+": %{customdata[1]}<br>",
                   name='neutral_comment',
                   showlegend=False
                   ),
        row=1,
        col=1)
    fig.add_trace(go.Scatter(x=df_pos.index, y=df_pos['sum_pre'],
                             customdata=np.transpose([df_pos[custom[0]], df_pos[custom[1]],
                                                      ]),
                             hovertemplate="<br>time: %{x}<br>" +
                             "Total comments: %{y}<br>" +
                             hover[0]+": %{customdata[0]}<br>" +
                             # hover[2]+": %{customdata[2]}<br>"
                             # hover[3]+": %{customdata[3]}<br>"
                             hover[1]+": %{customdata[1]}<br>",
                             name='neutral_comment',
                             showlegend=False
                             ),
                  row=1,
                  col=1)

    fig.add_trace(
        go.Bar(x=df_bar.index,
               y=df_bar["sum"],
               customdata=np.transpose([df_bar['predict_negative'],
                                        df_bar['predict_positive'], df_bar['predict_neutral']]),
               hovertemplate="<br>time: %{x}<br>" +
               "Total comments: %{y}<br>" +
               "Negative: %{customdata[0]}<br>" +
               "Positive: %{customdata[1]}<br>" +
               "Neutral: %{customdata[2]}",
               name='comment_in_day',
               showlegend=False,
               marker_color='blueviolet'),
        row=3,
        col=1)

    fig.update_xaxes(
        tickfont=dict(size=15, family='monospace', color='#B8B8B8'),
        tickmode='array',
        ticklen=6,
        showline=False,
        showgrid=False,
        gridcolor='#595959',
        ticks='outside')
    fig.update_layout(
        spikedistance=100,
        xaxis_rangeslider_visible=False,
        hoverdistance=1000)
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
        showline=True,
        #ticksuffix = '$',
        showgrid=False,
        gridcolor='#595959',
        ticks='outside')
    fig.update_layout(
        width=1900,
        height=1000,
        font_family='monospace',
        xaxis=dict(rangeselector=dict(buttons=date_buttons)),
        updatemenus=[dict(type='dropdown',
                          x=1.0,
                          y=1.108,
                          showactive=True,
                          active=2,
                          )],
        title=dict(text='<b>Sentiment Analysis<b>',
                   font=dict(color='#FFFFFF', size=22),
                   x=0.50),
        font=dict(color="orangered"),
        annotations=[
            dict(text="<b>Choose Cryptocurrency: <b>",
                 font=dict(size=20, color="#ffffff"),
                 showarrow=False,
                 x=1.02,
                 y=1.20,
                 xref='paper', yref="paper",
                 align="left"),
            dict(text="<b>Candlestick Chart <b>",
                 font=dict(size=20,  color="#ffffff"),
                 showarrow=False,
                 x=1.02,
                 y=1.20,
                 xref='paper', yref="paper",
                 align="left"),
            # dict( text = "<b>Price Chart<b>",
            #      font = dict(size = 20,  color = "#ffffff"),
            #      showarrow=False,
            #      x = 0.82,
            #     y = 0.285,
            #     xref = 'paper', yref = "paper",
            #     align = "left"),
            dict(text="<b>Volume Traded<b>",
                 font=dict(size=20,  color="#ffffff"),
                 showarrow=False,
                 x=0.14,
                 y=-0.53,
                 xref='paper', yref="paper",
                 align="left"),
            dict(text="<b>Relative Strength Index (RSI)<b>",
                 font=dict(size=20,  color="#ffffff"),
                 showarrow=False,
                 x=0.94,
                 y=-0.53,
                 xref='paper', yref="paper",
                 align="left")
        ],
        template="plotly_white",
        yaxis_showgrid=False,
        xaxis_showgrid=False
    )
    fig.layout["xaxis3"]["rangeslider"]["borderwidth"] = 4
    fig.layout["xaxis3"]["rangeslider"]["bordercolor"] = "blueviolet"
    fig.layout["yaxis3"]["ticksuffix"] = ""
    return fig


# In[11]:


def all_1_func(df_bar, df_neg, df_pos, df_neu, hover, custom):
    START_DATE = "2015-11-15"  # start date for historical data
    RSI_TIME_WINDOW = 7  # number of days

    # plot
    fig = make_subplots(rows=3,
                        cols=1,
                        shared_xaxes=True,
                        specs=[[{"rowspan": 2}], [{"rowspan": 1}], [{}]]
                        )
    date_buttons = [
        {'step': "all", 'label': "All time"},
        {'count':  1, 'step': "year", 'stepmode': "backward", 'label': "Last Year"},
        {'count':  1, 'step': "year", 'stepmode': "todate", 'label': "Current Year"},
        {'count':  6, 'step': "month", 'stepmode': "backward", 'label': "Last 6 Months"},
        {'count':  1, 'step': "month", 'stepmode': "todate", 'label': "Current Month"},
        {'count':  7, 'step': "day", 'stepmode': "todate", 'label': "Current Week"},
        {'count':  4, 'step': "day", 'stepmode': "backward", 'label': "Last 4 days"},
        {'count':  1, 'step': "day", 'stepmode': "backward", 'label': "Today"},
    ]

    fig.add_trace(go.Scatter(x=df_neu.index, y=df_neu['sum_pre'],
                             hovertemplate="<br>time: %{x}<br>" +
                             # hover[0]+": %{customdata[0]}<br>"
                             # hover[1]+": %{customdata[1]}<br>"
                             # hover[2]+": %{customdata[2]}<br>"
                             # hover[3]+": %{customdata[3]}<br>"
                             "comments of "+hover[0]+" : %{y}<br>",
                             name='neutral_comment',
                             showlegend=False
                             ),
                  row=1,
                  col=1)

    fig.add_trace(
        go.Scatter(x=df_neg.index, y=df_neg['sum_pre'],
                   hovertemplate="<br>time: %{x}<br>" +
                   # hover[0]+": %{customdata[0]}<br>"+
                   # hover[1]+": %{customdata[1]}<br>"
                   # hover[2]+": %{customdata[2]}<br>"
                   # hover[3]+": %{customdata[3]}<br>"
                   "comments of "+hover[0]+" : %{y}<br>",
                   name='neutral_comment',
                   showlegend=False
                   ),
        row=1,
        col=1)
    fig.add_trace(go.Scatter(x=df_pos.index, y=df_pos['sum_pre'],
                             hovertemplate="<br>time: %{x}<br>" +
                             # hover[0]+": %{customdata[0]}<br>"+
                             # hover[1]+": %{customdata[1]}<br>"
                             # hover[2]+": %{customdata[2]}<br>"
                             # hover[3]+": %{customdata[3]}<br>"
                             "comments of "+hover[0]+" : %{y}<br>",
                             name='neutral_comment',
                             showlegend=False
                             ),
                  row=1,
                  col=1)

    fig.add_trace(
        go.Bar(x=df_bar.index,
               y=df_bar["sum"],
               customdata=np.transpose([df_bar['predict_negative'],
                                        df_bar['predict_positive'], df_bar['predict_neutral']]),
               hovertemplate="<br>time: %{x}<br>" +
               "num_comments: %{y}<br>" +
               "Negative: %{customdata[0]}<br>" +
               "Positive: %{customdata[1]}<br>" +
               "Neutral: %{customdata[2]}",
               name='comment_in_day',
               showlegend=False,
               marker_color='blueviolet'),
        row=3,
        col=1)

    fig.update_xaxes(
        tickfont=dict(size=15, family='monospace', color='#B8B8B8'),
        tickmode='array',
        ticklen=6,
        showline=False,
        showgrid=False,
        gridcolor='#595959',
        ticks='outside')
    fig.update_layout(
        spikedistance=100,
        xaxis_rangeslider_visible=False,
        hoverdistance=1000)
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
        showline=True,
        #ticksuffix = '$',
        showgrid=False,
        gridcolor='#595959',
        ticks='outside')
    fig.update_layout(
        width=1900,
        height=1000,
        font_family='monospace',
        xaxis=dict(rangeselector=dict(buttons=date_buttons)),
        updatemenus=[dict(type='dropdown',
                          x=1.0,
                          y=1.108,
                          showactive=True,
                          active=2,
                          )],
        title=dict(text='<b>Sentiment Analysis<b>',
                   font=dict(color='#FFFFFF', size=22),
                   x=0.50),
        font=dict(color="orangered"),
        annotations=[
            dict(text="<b>Choose Cryptocurrency: <b>",
                 font=dict(size=20, color="#ffffff"),
                 showarrow=False,
                 x=1.02,
                 y=1.20,
                 xref='paper', yref="paper",
                 align="left"),
            dict(text="<b>Candlestick Chart <b>",
                 font=dict(size=20,  color="#ffffff"),
                 showarrow=False,
                 x=1.02,
                 y=1.20,
                 xref='paper', yref="paper",
                 align="left"),
            # dict( text = "<b>Price Chart<b>",
            #      font = dict(size = 20,  color = "#ffffff"),
            #      showarrow=False,
            #      x = 0.82,
            #     y = 0.285,
            #     xref = 'paper', yref = "paper",
            #     align = "left"),
            dict(text="<b>Volume Traded<b>",
                 font=dict(size=20,  color="#ffffff"),
                 showarrow=False,
                 x=0.14,
                 y=-0.53,
                 xref='paper', yref="paper",
                 align="left"),
            dict(text="<b>Relative Strength Index (RSI)<b>",
                 font=dict(size=20,  color="#ffffff"),
                 showarrow=False,
                 x=0.94,
                 y=-0.53,
                 xref='paper', yref="paper",
                 align="left")
        ],
        template="plotly_white",
        yaxis_showgrid=False,
        xaxis_showgrid=False
    )
    fig.layout["xaxis3"]["rangeslider"]["borderwidth"] = 4
    fig.layout["xaxis3"]["rangeslider"]["bordercolor"] = "blueviolet"
    fig.layout["yaxis3"]["ticksuffix"] = ""
    return fig


# In[12]:

def line_chart(base):
    df_bar, df_neg, df_pos, df_neu, hover, custom = data_line(base)
    len_col = len(custom)
    if len_col == 4:
        fig = all_4_func(df_bar, df_neg, df_pos, df_neu, hover, custom)
    elif len_col == 3:
        fig = all_3_func(df_bar, df_neg, df_pos, df_neu, hover, custom)
    elif len_col == 2:
        fig = all_2_func(df_bar, df_neg, df_pos, df_neu, hover, custom)
    else:
        fig = all_1_func(df_bar, df_neg, df_pos, df_neu, hover, custom)

    return fig


# In[ ]:
