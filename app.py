from flask import Flask, render_template, request
import json
import plotly
from input_func import model_detect
from layout import piechart_layout, linechart_layout, home_layout
from layout import tsne_scatter_plot_combine, test, w2v_model  # (model, word)
from dash_application import create_dash_application, create_dash_application_line, create_dash_application_pie


app = Flask(__name__)
base = ""
word = ""

app.config['suppress_callback_exceptions'] = True

theme = {
    'dark': True,
    'detail': '#2d3038',  # Background-card
    'primary': '#007439',  # Green
    'secondary': '#FFD15F',  # Accent
}

base_1 = './caphe_sen_pie.xlsx'
dash_app = create_dash_application(app)
dash_app_line = create_dash_application_line(app)
dash_app_line.layout = linechart_layout(base_1)
dash_app_pie = create_dash_application_pie(app)
dash_app_pie.layout = piechart_layout(base_1)
model, vocabulary = w2v_model(base_1)


@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    global word
    key = request.form['word']
    cato = request.form['category']
    content = request.form.getlist('web_crawling')
    print(content)
    cato1 = model_detect(key)
    if cato == cato1:
        cato2 = "True"
    else:
        cato2 = "False"
    if 'shopee' in content:
        print('Crawling Shopee')
    if 'lazada' in content:
        print('Crawling Lazada')
    if 'tiki' in content:
        print('Crawling Tiki')
    if 'vozforum' in content:
        print('Crawling Vozforum')
    if 'twitter' in content:
        print('Crawling Twitter')
    if 'tinhte' in content:
        print('Crawling TinhTe')
    return render_template('dash_home.html', value=key, value1=cato2,
                           value2=cato, value3=cato1, val=content)


@app.route("/dash", methods=['GET', 'POST'])
def dash():
    print('chart')
    dash_app.layout = home_layout()
    return dash_app


@app.route("/dash/linechart", methods=['GET', 'POST'])
def dashline():
    return dash_app_line


@app.route("/dash/piechart", methods=['GET', 'POST'])
def dashpie():
    # base_1='caphe_sen_pie.xlsx'
    return dash_app_pie


@app.route('/dash/chart3D/callback', methods=['POST', 'GET'])
def cb():
    return gm(request.args.get('data'))


@app.route('/dash/chart3D')
def index():
    if test == 'No':
        return render_template('no_tsne.html')  # ,  graphJSON=gm())
    else:
        return render_template('dash3D.html')


def gm(text):
    text = text.replace(' ', '_')
    fig = tsne_scatter_plot_combine(text, model, vocabulary)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def vocab():
    return gm(request.args.get('data'))


#     dash_app.layout=tsne_scatter_plot_combine(word,base)
#     return redirect(url_for('dash'))

if __name__ == "__main__":
    app.run(debug=True)
