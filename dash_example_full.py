# In[]:
# Import required libraries

import os
import dash
import dash_core_components as core
import dash_html_components as html
from dash.dependencies import Input, Output
from flask_caching import Cache
import quantmod as qm


# In[]:
# Create layout

app = dash.Dash("Stock market app")
app.css.append_css({
    'external_url': (
        'https://rawgit.com/chriddyp/0247653a7c52feb4c48437e1c1837f75'
        '/raw/a68333b876edaf62df2efa7bac0e9b3613258851/dash.css'
    )
})

# Add caching
cache = Cache(app.server, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL', '127.0.0.1:6379')
})
timeout = 60 * 60  # 1 hour

app.layout = html.Div(
    [
        html.H1('Quantmod Demo | 5-minute App'),
        html.Div([
            html.Span(
                core.Dropdown(
                    id='dropdown',
                    options=[
                        dict(label='PowerShares QQQ Trust Series 1', value='QQQ'),
                        dict(label='SPDR S&P 500 ETF Trust', value='SPY'),
                        dict(label='Apple Inc', value='AAPL'),
                        dict(label='Goldman Sachs Group Inc', value='GS'),
                    ],
                    value='SPY',
                ), style={'width': '400px', 'display': 'inline-block'}
            ),
            html.Span(
                core.Dropdown(
                    id='multi',
                    options=[
                        dict(label='EMA', value='EMA'),
                        dict(label='RSI', value='RSI'),
                        dict(label='MACD', value='MACD'),
                        dict(label='BBANDS', value='BBANDS'),
                    ],
                    multi=True,
                    value=['EMA']
                ), style={'width': '400px', 'display': 'inline-block'}
            )
        ]),
        html.Div([
            html.Div([
                html.Label('EMA Variable'),
                core.Input(id='ema-slider')
            ], id='ema-controls', style={'display': 'none'}),
            html.Div([
                html.Label('RSI Variable'),
                core.Input(id='rsi-slider')
            ], id='rsi-controls', style={'display': 'none'})
        ]),
        core.Graph(id='output', style={'width': '100%'})
    ], style={'width': '90%', 'margin-left': 'auto', 'margin-right': 'auto'}
)


@app.callback(Output('ema-controls', 'style'), [Input('multi', 'value')])
def display_ema_control(selected_values):
    if selected_values is None:
        return {'display': 'none'}
    elif 'EMA' in selected_values:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(Output('rsi-controls', 'style'), [Input('multi', 'value')])
def display_ema_control(selected_values):
    if selected_values is None:
        return {'display': 'none'}
    elif 'RSI' in selected_values:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(Output('output', 'figure'), [Input('dropdown', 'value'),
                                           Input('multi', 'value'),
                                           Input('rsi-slider', 'value'),
                                           Input('ema-slider', 'value')])
@cache.memoize(timeout=timeout)
def update_graph_from_dropdown(dropdown, multi, rsi_value, ema_value):
    print(rsi_value)
    print(ema_value)
    # Get Quantmod Chart
    ch = qm.get_symbol(dropdown, start='2016/01/01')

    if 'EMA' in multi:
        ch.add_EMA()
    if 'RSI' in multi:
        ch.add_RSI()
    if 'MACD' in multi:
        ch.add_MACD()
    if 'BBANDS' in multi:
        ch.add_BBANDS()

    # Return plot as figure
    fig = ch.to_figure()
    return fig


# In[]:
# Main

if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
