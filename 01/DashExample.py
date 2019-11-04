import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import requests 
import dash_daq as daq
import time
from datetime import datetime

def GetData():
    #get market data
    URL = "https://poloniex.com/public?command=returnTicker"
    r = requests.get(url = URL) 
    coin_data = r.json() 
    k = list(coin_data.keys())
    dk = coin_data[k[0]].keys()

    data = []
    for c in k:
        dummy = []
        sc = c.split("_")
        dummy.append(sc[0])
        dummy.append(sc[1])
        for i in dk:
            dummy.append(coin_data[c][i])
        data.append(dummy)

    dk = list(dk)
    dk = ['to']+dk
    dk = ['from']+dk

    df = pd.DataFrame(data, columns = dk)
    return df

external_stylesheets = ['https://codepen.io/anon/pen/mardKv.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    #top row
    html.Div(children = [
    #main table
    dash_table.DataTable(
    selected_rows=[2],
    fixed_rows={ 'headers': True, 'data': 0 },
    style_table={'max_height':900,'overflowY':'scroll'},
    id = 'MainTable',
    row_selectable='single',
    sort_action='native',
    style_header={'backgroundColor': 'rgb(30, 30, 30)'},
    style_cell={'backgroundColor': 'rgb(50, 50, 50)','color': 'white'},
    columns=[{"name": i, "id": i} for i in GetData().columns],
    data=GetData().to_dict('records')),
    dcc.Interval(
            id='interval-component',
            interval=1*5000, # in milliseconds
            n_intervals=0
        ),
    #show candle of selected
    html.Div(id='candle_selected',
    children=[dcc.Graph(id="candle_selected_graph",
    #figure={'data' : [trace]},
    style={"height" : "80vh", "width" : "100%"})],
    style={'columnCount': 1})
    ], id = 'id_1')
])

@app.callback(Output('MainTable', 'data'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    return GetData().to_dict('records')

@app.callback(Output('candle_selected_graph', 'figure'),
              [Input('MainTable', 'selected_rows')],
              [State('MainTable', 'data')]) # this doesnt trigger the function
def PrintCandle(n,data):
    currencyPair = data[n[0]]['from'] + "_" + data[n[0]]['to']
    t = time.time()
    end_time = int(t)
    start_time = end_time - 14400*400
    URL = "https://poloniex.com/public?command=returnChartData&currencyPair="+str(currencyPair)+"&start="+str(start_time)+"&end="+str(end_time)+"&period=14400"
    r = requests.get(url = URL) 
    d = r.json()
    h = []
    l = []
    o = []
    c = []
    da = []
    print(URL)
    for i in d:
        da.append(datetime.utcfromtimestamp(i['date']).strftime('%Y-%m-%d %H:%M:%S'))
        h.append(i['high'])
        l.append(i['low'])
        o.append(i['open'])
        c.append(i['close'])


    trace = go.Candlestick(x=da,open=o,high=h,low=l,close=c,increasing={'line': {'color': '#00CC94'}},decreasing={'line': {'color': '#F50030'}})
    return {'data': [trace],'layout':{
                    'title':'Price for currency-pair '+str(currencyPair),
                    'xaxis':{
                        'title':'time'
                    },
                    'yaxis':{
                        'title':'price'
                    }
                }}


if __name__ == '__main__':
    app.run_server(debug=True)