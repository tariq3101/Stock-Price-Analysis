import datetime
import yfinance as yf
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State, ALL

app = dash.Dash(__name__)
app.title = "Stock Visualization"
app.layout = html.Div(children=[
    html.H1("Stock Visualization Dashboard"),
    
    html.H4("Please enter a stock name"),
    dcc.Input(id='input-single', value='WIT', type='text'),
    
    html.Button('Submit Single Stock', id='submit-single', n_clicks=0),
    html.Div(id='output-graph-single'),
    
    html.H4("Please enter three stock names (comma-separated) for comparison"),
    dcc.Input(id='input-compare', value='AAPL,MSFT,WIPRO.NS', type='text'),
    
    html.Button('Submit Comparison Stocks', id='submit-compare', n_clicks=0),
    html.Div(id='output-graph-compare'),

    html.Link(rel="stylesheet", href="/assets/style.css"),
])


def generate_graph(stock_data, title):
    return {
        'data': [{'x': stock_data.index, 'y': stock_data['High'], 'type': 'line', 'name': title}],
        'layout': {'title': title}
    }


@app.callback(
    Output(component_id='output-graph-single', component_property='children'),
    [Input('submit-single', 'n_clicks')],
    [State('input-single', 'value')]
)
def update_single_graph(n_clicks, input_single):
    if n_clicks > 0:
        start = datetime.datetime(2010, 1, 1)
        end = datetime.datetime.now()
        
        try:
            df_single = yf.download(input_single, start, end)
            graph_single = dcc.Graph(id="graph-single", className="graph-container", figure=generate_graph(df_single, input_single))
        except:
            graph_single = html.Div("Error retrieving stock data for single stock.")
        
        return graph_single
    else:
        return None


@app.callback(
    Output(component_id='output-graph-compare', component_property='children'),
    [Input('submit-compare', 'n_clicks')],
    [State('input-compare', 'value')]
)
def update_compare_graph(n_clicks, input_compare):
    if n_clicks > 0:
        start = datetime.datetime(2010, 1, 1)
        end = datetime.datetime.now()

        try:
            stocks_to_compare = [stock.strip() for stock in input_compare.split(',')]
            df_compare = yf.download(stocks_to_compare, start, end)['High']
            data_compare = [{'x': df_compare.index, 'y': df_compare[stock], 'type': 'line', 'name': stock} for stock in stocks_to_compare]
            graph_compare = dcc.Graph(id="graph-compare", figure={'data': data_compare, 'layout': {'title': 'Stock Comparison'}})
        except:
            graph_compare = html.Div("Error retrieving stock data for comparison.")
        
        return graph_compare
    else:
        return None


if __name__ == '__main__':
    app.run_server()
