# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
from collections import OrderedDict
from dash.dependencies import Input, Output, State
from stockstats import StockDataFrame as Sdf
import dash_bootstrap_components as dbc
import dash_table as dt
import yfinance as yf
import plotly.graph_objs as go
from datetime import datetime, timedelta
#import pickle
import random
import numpy as np
import pandas as pd
import plotly.io as pio
import plotly.express as px
import statistics
import datetime
import json
import talib
import vectorbt as vbt

# defining style color
colors = {"background": "#151519", "text": "#ffFFFF"}

# Define the path to the Excel file
file_path = 'Yahoo Ticker Symbols.xlsx'

# Read the Excel file into a DataFrame
df = pd.read_excel(file_path)

countries_list = df['Country'].unique()

index_list = df[df['Country'] == 'USA']['Exchange'].unique()

category_list = np.sort(df[df['Exchange'] == 'NYQ'].dropna()['Category Name'].unique())

ticker_list = np.sort(df[df['Exchange'] == 'NYQ']['Ticker'].unique())
    
patterns = talib.get_function_groups()['Pattern Recognition']

entry_patterns = [
    'CDLHAMMER',
    'CDLINVERTEDHAMMER',
    'CDLPIERCING',
    'CDLMORNINGSTAR',
    'CDL3WHITESOLDIERS'
]

exit_patterns = [
    'CDLHANGINGMAN',
    'CDLSHOOTINGSTAR',
    'CDLEVENINGSTAR',
    'CDL3BLACKCROWS',
    'CDLDARKCLOUDCOVER'
]

def get_candlesticks_patterns(symbols):
    # Set the stock symbol and start/end dates for data retrieval
    #symbols = ['A'] ['GAFL-CRA1DB0.SA', 'ITSA4.SA', 'BRML-DEB12L0.SA', 'OSEC-CRA24L1.SA', 'TAXA342.SA', 'LEVE3.SA', 'RBCS-CRI03B0.SA', 'CSCO34.SA', 'TAXA356.SA', 'TAXA94L.SA', 'AXPB34.SA', 'ESTC3.SA', 'TAXA35.SA', 'TRIS3.SA', 'BSCS-CRII40B.SA', 'BNDP-DEB61B0.SA', 'TAXA256.SA', 'MWET3.SA', 'GGBR4.SA', 'AELP3F.SA', 'EDFO11B.SA', 'FBOK34.SA', 'TAXA349.SA', 'TAXA19L.SA', 'TAXA323.SA', 'GAFL-CRAA2B0.SA', 'POMO3.SA', 'PDGS-CRI15L1.SA', 'BGIP4.SA', 'TAXA124.SA', 'PTNT3.SA', 'TAXA166.SA', 'TAXA107.SA', 'PABY11.SA', 'OPRE1B.SA', 'TAXA23L.SA', 'CRUZ3.SA', 'KNRI11.SA', 'DOHL3F.SA', 'SLED3.SA', 'RANI3.SA', 'PRSN11B.SA', 'TAXA238.SA', 'TAXA263.SA', 'FVBI11B.SA', 'TAXA81L.SA', 'VERZ34F.SA', 'ENBR-DEB43L0.SA', 'TAXA355.SA', 'UNAG-FIDS10B.SA', 'MMMC34F.SA', 'COTY34F.SA', 'RNEW11.SA', 'BVLS-DEB11B0.SA', 'TAXA36.SA', 'ICON11.SA', 'NPPF-FID010B.SA', 'FAMB11B.SA', 'RDVT-DEB11B0.SA', 'VVAR11.SA', 'MMXM11.SA', 'TAXA302.SA', 'TAXA184.SA', 'SNSL3F.SA', 'DAGB33.SA', 'OVSA-DEB31L1.SA', 'ESTR3F.SA', 'TAXA75.SA', 'XTED11.SA', 'BNDP-DEB61L0.SA', 'UNID-DEB21L0.SA', 'GAIA-CRI5BL0.SA', 'GSGI34F.SA', 'QCOM34F.SA', 'CSAB3.SA', 'TAXA264.SA', 'TAXA81.SA', 'TAXA145.SA', 'LUXM3F.SA', 'BSCS-CRII5L0.SA', 'USBC34.SA', 'WPLZ11B.SA', 'GAFL-CRA31L1.SA', 'GFSA-DEB82L0.SA', 'BSCS-CRIJ0L0.SA', 'CELP5.SA', 'CGAS-DEB33L0.SA', 'BSCS-CRIO6L0.SA', 'EVEN3.SA', 'HGLG11.SA', 'JOPA3.SA', 'TAXA305.SA', 'PIBB.SA', 'TAXA72L.SA', 'XRXB34F.SA', 'RUMO9.SA', 'GAFL-CRA11L1.SA', 'TAXA86L.SA', 'RBCS-CRI85L0.SA', 'TAXA96.SA', 'MGIP-DEB31B0.SA', 'BRAP3.SA', 'FIGE3F.SA', 'TAXA97.SA', 'BDLS-DEB11L1.SA', 'KLBN-DCA61L0.SA', 'CXTL11.SA', 'BRGE12.SA', 'PFIZ34F.SA', 'MSFT34.SA', 'RBRA-CRI68L1.SA', 'CBMA3F.SA', 'FIRM5L.SA', 'SOND3.SA', 'TAXA20.SA', 'UPSS34.SA', 'TAXA92.SA', 'CTVL5L.SA', 'RNEW3.SA', 'BRPR-DEB11B0.SA', 'ABCB10F.SA', 'RCTA6L.SA', 'EBEN-DEB41B0.SA', 'SBSP-DEB7BL0.SA', 'BSCS-CRIS70B.SA', 'TAXA121.SA', 'BVLS-DEB41B0.SA', 'CGAS-DEB42L0.SA', 'GUAR4.SA', 'ENGI-DEB76B0.SA', 'VIGR3.SA', 'ICO211.SA', 'CMCS34F.SA', 'TAXA57L.SA', 'WTVP-CRI11L1.SA', 'TAXA68.SA', 'PMSP12BL.SA', 'SWET3.SA', 'BBRC11.SA', 'STEN-DEB31L0.SA', 'CSRN5F.SA', 'TAXA0L.SA', 'ITEC3.SA', 'CEBR5.SA', 'MMMC34.SA', 'MERC3F.SA', 'SCPF11.SA', 'RBRA-CRI93L1.SA', 'BBSD.SA', 'GAIA-CRI5BL1.SA', 'CMGD-DEB21L1.SA', 'RBCS-CRI97B0.SA', 'CMGD-DEB33L0.SA', 'PDGR-DCA81B0.SA', 'KMBB34.SA', 'GAIA-CRI780B.SA', 'UTIL11.SA', 'PLAS3F.SA', 'CBMA3.SA', 'ABCB10L.SA', 'SOND6.SA', 'IVBX11.SA', 'GETI4.SA', 'COLN-DEB43L0.SA', 'TAXA233.SA', 'GDBR34.SA', 'IFIX11.SA', 'GAFL-CRA1DL1.SA', 'TAXA191.SA', 'RBCS-CRI97L1.SA', 'TAXA285.SA', 'BSCS-CRIS7B0.SA', 'BRGE8F.SA', 'GWIR11.SA', 'WHRL4.SA', 'TAXA309.SA', 'TAXA139.SA', 'RCSL4.SA', 'CMGD-DEB31L1.SA', 'CSMO11.SA', 'AGSA5L.SA', 'CGAS-DEB32L0.SA', 'TAXA49.SA', 'TAXA221.SA', 'CTIP3.SA', 'SCLO4F.SA', 'CELP7.SA', 'MOSC34F.SA', 'SBSP-DEB7BB0.SA', 'TAXA67L.SA', 'DBEN-DEB420B.SA', 'TAXA320.SA', 'DBEN-DEBE6B0.SA', 'TAXA34L.SA', 'VALE-DEB84L0.SA', 'VALE-DEB84L1.SA', 'WALM34.SA', 'OIBR-DEB92L0.SA', 'RAPT3.SA', 'POSI3.SA']
    
    print(symbols)
    
    start_date = datetime.date.today() - timedelta(days=5)
    
    # Retrieve the stock data
    df_patterns = pd.DataFrame(columns=['ticker', 'pattern', 'market'])
    
    # Get the candlestick patterns to check
    patterns = talib.get_function_groups()['Pattern Recognition']
    
    stock_data = yf.download(symbols, start=start_date)
    
    if len(symbols) == 1:
        multi_col = pd.MultiIndex.from_arrays([stock_data.columns, symbols*len(stock_data.columns)], names=('', 'Symbol'))
        stock_data.columns = multi_col
    
    # Calculate the number of non-NaN values in each column
    counts = stock_data.count()
    
    # Count the number of unique values in each column
    unique_counts = stock_data.nunique()
    
    # Drop the columns where the number of unique values is 1
    cols_to_drop = unique_counts[unique_counts < 3].index
    stock_data = stock_data.drop(cols_to_drop, axis=1)
    
    #if len(ticker) > 100:
    #    for i in range(101, len(ticker), 100):
    #        df_prices = df_prices.append(yf2.download(ticker[i:i+100],  start = datetime.date.today()- timedelta(days= 252), end = datetime.date.today())['Close'])
        
    stock_data = stock_data.dropna(axis=1, how='all')
    
    failed_downloads = list(set(symbols) - set(stock_data.columns.unique(level=1)))
    
    lst = ['Open', 'High', 'Low', 'Close']
    #list_patterns = {}
    # Loop through the patterns and check if they appear on the last day of the stock
    for symbol in stock_data.columns.unique(level=1):
        print(symbol)
        for pattern in patterns:
            
            dt = stock_data.loc[:, stock_data.columns.get_level_values(1) == symbol]
            
            if set(lst).issubset(set(dt.columns.unique(level=0))):
                pattern_values = getattr(talib, pattern)(dt['Open'].values.reshape(-1), dt['High'].values.reshape(-1), dt['Low'].values.reshape(-1), dt['Close'].values.reshape(-1))
                #print(pattern_values)
                if pattern_values[-1] != 0:
                    market = 'BULL' if pattern_values[-1] > 0 else 'BEAR' if pattern_values[-1] < 0 else ''
                    #list_patterns[symbol] = [pattern[3:], '✅', market] #if pattern_values[-1] != 0 else ['❌', market] 
                    new_row = {'ticker': symbol, 'pattern': pattern[3:], 'market': market}
                    df_patterns = df_patterns.append(new_row, ignore_index=True)
                #if pattern_values[-1] != 0:
                #    print(f"{pattern} pattern detected on {end_date} for {symbol}.")

    return df_patterns

start_date = datetime.date.today() - timedelta(days=10 * 365)
end_date = datetime.date.today()

'''
df = yf.download('AAPL', start=start_date)
entry_patterns = [
    'CDLHAMMER',
    'CDLINVERTEDHAMMER',
    'CDLPIERCING',
    'CDLMORNINGSTAR',
    'CDL3WHITESOLDIERS'
]
exit_patterns = [
    'CDLHANGINGMAN',
    'CDLSHOOTINGSTAR',
    'CDLEVENINGSTAR',
    'CDL3BLACKCROWS',
    'CDLDARKCLOUDCOVER'
]
fees = 0.00001
slippage = 0.005
direction = 'LongOnly'
'''

def backtesting(df, entry_patterns, exit_patterns, fees, slippage, direction, initial_cash):

    dt_patterns_names = [0]*len(df)

    dt_entries = pd.DataFrame()
    for pattern in entry_patterns:
        pattern_values = getattr(talib, pattern)(df['Open'], df['High'], df['Low'], df['Close'])
        dt_entries = pd.concat([dt_entries, pattern_values], axis=1)
        pattern_values[pattern_values != 0] = pattern[3:]
        dt_patterns_names = np.where(pattern_values != 0, pattern_values, dt_patterns_names)
        
    dt_exits = pd.DataFrame()
    for pattern in exit_patterns:
        pattern_values = getattr(talib, pattern)(df['Open'], df['High'], df['Low'], df['Close'])
        dt_exits = pd.concat([ dt_exits, pattern_values], axis=1)
        pattern_values[pattern_values != 0] = pattern[3:]
        dt_patterns_names = np.where(pattern_values != 0, pattern_values, dt_patterns_names)
        
    df['pattern_names'] = dt_patterns_names
    
    # create a sum column that sums all other columns
    dt_entries['sum'] = dt_entries.apply(lambda row: row.sum(), axis=1)
    dt_exits['sum'] = dt_exits.apply(lambda row: row.sum(), axis=1)
    
    # create a positive column that shows positive cells of the sum column
    dt_entries['positive'] = dt_entries.apply(lambda row: row['sum'] if row['sum'] > 0 else 0, axis=1)
    dt_exits['positive'] = dt_exits.apply(lambda row: row['sum'] if row['sum'] > 0 else 0, axis=1)
    
    # create a negative column that shows negative cells of the sum column
    dt_entries['negative'] = dt_entries.apply(lambda row: row['sum'] if row['sum'] < 0 else 0, axis=1)
    dt_exits['negative'] = dt_exits.apply(lambda row: row['sum'] if row['sum'] < 0 else 0, axis=1)   
    
    df['entry_signal'] = dt_entries['positive'] > 0
    
    df['exit_signal'] =  dt_exits['negative'] < 0
    
    df['short_entry_signal'] = dt_entries['negative'] < 0
    
    df['short_exit_signal'] = dt_exits['positive'] > 0
    
    position = vbt.Portfolio.from_signals(
        df['Close'], 
        entries = df['entry_signal'] if direction == 'LongOnly' or direction == 'Both' else None, 
        exits = df['exit_signal'] if direction == 'LongOnly' or direction == 'Both' else None,
        short_entries= df['short_entry_signal'] if direction == 'ShortOnly' or direction == 'Both' else None,
        short_exits = df['short_exit_signal'] if direction == 'ShortOnly' or direction == 'Both' else None,
        direction=direction,
        init_cash=initial_cash,
    )
    
    df['returns'] = position.returns()
    
    
    return position, df, position.positions.records_readable



external_stylesheets = [dbc.icons.FONT_AWESOME, dbc.themes.SLATE]

# adding css
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, prevent_initial_callbacks='initial_duplicate')
server = app.server
app.layout = html.Div(
    style={"backgroundColor": "#000000"},
    children=[
        dcc.Download(id="download-file"),
        html.Div(
            [  # header Div
             dbc.Row(
                 [
                    dbc.Col(
                        [
                            html.Label(
                                "Candlestick patterns",
                                style={
                                    'font-size': '18px',
                                    'padding-bottom': '5px',
                                },
                            ),
                            html.Label(
                                "Candlestick patterns use candle shapes and positions to predict future price movements, providing valuable information about market sentiment for traders and investors.",
                                style={
                                    'font-size': '12px',
                                    'font-weight': "lighter",
                                },
                            ),
                        ],
                        style={
                            "color": colors["text"],
                            'font-family':'montserrat',
                            'font-size': '18px',
                        },
                        width={'size':7}
                    ),
                    dbc.Col(
                        [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Row(
                                        [
                                        html.Label(
                                            "Yann Krautz",
                                            style={
                                                "textAlign": "right",
                                                "color": colors["text"],
                                                'font-family':'montserrat',
                                                #"padding": "5px 0px 0px 55px",
                                                'font-size': '16px',
                                                'padding-top': '2px',
                                            },
                                        ),
                                        html.Br(),
                                        dbc.Row(
                                            [
                                                html.A(
                                                    html.I(className="fas fa-brands fa-github"), 
                                                    href='https://github.com/Yann-Krautz',
                                                    target='_blank',
                                                    style={
                                                        "color": "white",
                                                        "padding": "5px",
                                                    },
                                                ),
                                                html.A(
                                                    html.I(className="fas fa-solid fa-globe"),
                                                    href='https://yannsouza.myportfolio.com/',
                                                    target='_blank',
                                                    style={
                                                        "color": "white",
                                                        "padding": "5px",
                                                    },
                                                ), 
                                                html.A(
                                                    html.I(className="fas fa-brands fa-linkedin"),
                                                    href='https://www.linkedin.com/in/yann-krautz-souza-6156b0267/',
                                                    target='_blank',
                                                    style={
                                                        "color": "white",
                                                        "padding": "5px",
                                                    },
                                                    
                                                ),
                                                html.A(
                                                    html.I(className="fas fa-solid fa-envelope", title='yannksouza@gmail.com'),
                                                    style={
                                                        "color": "white",
                                                        "padding": "5px",
                                                    },
                                                ),
                                            ],
                                            style={
                                                'display': 'inline-block',
                                                'text-align': 'right',
                                                'padding': '0px',
                                            },
                                        ),
                                    ],
                                    ),
                                    style={
                                        #"background-color": "green",
                                        'display': 'flex',
                                        'align-items': 'right',
                                        'justify-content': 'right',
                                    },
                                    width={'size':10}
                                ),
                                dbc.Col(
                                    html.Div(
                                       html.Img(src=r'assets/fotoperfilyann.JPG', style={'height': '100%', 'width': '100%',  'object-fit': 'cover','border-radius': '50%'}),
                                       style={'height': '50px', 'width': '50px', 'border-radius': '50%', },
                                    ),
                                    style={
                                    },
                                    width={'size':2}
                                ),
                            ],
                            style={
                                "padding-top": "10px",
                            },
                        ),
                        ],
                        width={'size':5}
                    ),
                ],
                 style={
                     "color": colors["text"],
                     'font-family':'montserrat',
                     "padding": "20px 20px 0px 40px",
                 },
            ),
        ],
        ),
        html.Hr(style={"background-color": "white", 'height': '1px', 'border': 'none', 'opacity': '0.2',}),
        html.Div(
            [      
            dbc.Row(
                [
                    dbc.Col(
                        [             
                            html.Label(
                                "Country",
                                style={
                                    "textAlign": "center",
                                    "color": colors["text"],
                                    "margin": "10px 0px 10px 5px",
                                    'font-size': '14px',
                                    
                                },
                            ),
                            dcc.Dropdown(
                                id="country-dropdown",
                                options=[
                                    {
                                        "label": str(countries_list[i]),
                                        "value": str(countries_list[i]),
                                    }
                                    for i in range(len(countries_list))
                                ],
                                value="USA",#"AAL","DIS","DAL","AAPL","MSFT","CCL","GPRO","ACB","PLUG","AMZN"],
                                multi=False,
                                style={
                                    "background-color": "#151519",
                                    "color": colors["text"],
                                    #"color": "white",
                                    "border-style": "none",
                                    "border-radius": "15px",
                                },
                            ),
                        ],
                        style={'display': 'inline-block',},
                        width=2,
                    ),
                    dbc.Col(
                        [   
                            html.Label(
                                "Index",
                                style={
                                    "textAlign": "center",
                                    "color": colors["text"],
                                    "margin": "10px 0px 10px 5px",
                                    'font-size': '14px',
                                    
                                },
                            ),
                            html.Br(),
                            dbc.Row(
                                [
                                dbc.Col(
                                    [     
                                    dcc.Dropdown(
                                        id="index-dropdown",
                                        options=[
                                            {
                                                "label": str(index_list[i]),
                                                "value": str(index_list[i]),
                                            }
                                            for i in range(len(index_list))
                                        ],
                                        value=["NYQ",],#"AAL","DIS","DAL","AAPL","MSFT","CCL","GPRO","ACB","PLUG","AMZN"],
                                        multi=True,
                                        style={
                                            "background-color": "#151519",
                                            "color": colors["text"],
                                            #"color": "white",
                                            "border-style": "none",
                                            "border-radius": "15px",
                                            'padding-left': '2px',
                                            "margin-right": "0px",
                                        },
                                    ),
                                    ],
                                    width=11
                                ),
                                dbc.Col(
                                    [   
                                    html.Div(
                                        html.I(
                                            id='add-from-index',
                                            className="fas fa-solid fa-square-caret-down", 
                                            style={"color": "#4E51F5", "font-size": "20px", "margin-top": "8px", 'cursor': 'pointer'},
                                            title='Add all tickers within an index to the backtesting area. Note that if there are more than 200 tickers in the index, the system will randomly select 200 tickers for analysis.',
                                        ), 
                                    ),
                                    ],
                                    width=1,
                                    style={"padding": "0px",}
                                ),
                                ]
                            ),
                        ],
                        style={'display': 'inline-block',},
                        width=3,
                    ),
                    dbc.Col(
                        [   
                            html.Label(
                                "Category",
                                style={
                                    "textAlign": "center",
                                    "color": colors["text"],
                                    "margin": "10px 0px 10px 5px",
                                    'font-size': '14px',
                                    
                                },
                            ),
                            html.Br(),
                            dbc.Row(
                                [
                                dbc.Col(
                                    [     
                                        dcc.Dropdown(
                                            id="category-dropdown",
                                            options=[
                                                {
                                                    "label": str(category_list[i]),
                                                    "value": str(category_list[i]),
                                                }
                                                for i in range(len(category_list))
                                            ],
                                            #value=["NYQ",],#"AAL","DIS","DAL","AAPL","MSFT","CCL","GPRO","ACB","PLUG","AMZN"],
                                            multi=False,
                                            style={
                                                "background-color": "#151519",
                                                "color": colors["text"],
                                                "border-style": "none",
                                                "border-radius": "15px",
                                            },
                                        ),
                                    ],
                                    width=11
                                ),
                                dbc.Col(
                                    [   
                                    html.Div(
                                        html.I(
                                            id='add-from-category',
                                            className="fas fa-solid fa-square-caret-down", 
                                            style={"color": "#4E51F5", "font-size": "20px", "margin-top": "8px", 'cursor': 'pointer'},
                                            title='Add all tickers within a category to the backtesting area',
                                        ), 
                                    ),
                                    ],
                                    width=1,
                                    style={"padding": "0px",}
                                ),
                                ]
                            ),
                        ],
                        style={'display': 'inline-block',},
                        width=3,
                    ),   
                ],
                style={
                    "padding-left": "40px",
                    'font-family':'montserrat',
                    'font-weight': "lighter",
                },
            ),
            ],
        ),
        html.Hr(style={"background-color": "white", 'height': '1px', 'border': 'none', 'opacity': '0.2',}),
        html.Div(
            [  # Dropdown Div
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label(
                                    "Ticker",
                                    style={
                                        "textAlign": "left",
                                        "color": colors["text"],
                                        "margin": "0px 0px 10px 5px",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="ticker",
                                    options=[
                                        {
                                            "label": str(ticker_list[i]),
                                            "value": str(ticker_list[i]),
                                        }
                                        for i in range(len(ticker_list))
                                    ],
                                    multi=True,
                                    style={
                                        "background-color": "#151519",
                                        "color": colors["text"],
                                        "border-style": "none",
                                        "border-radius": "15px",
                                        "padding": "5px 5px 5px 10px",
                                    },
                                ),
                                html.Br(),
                                html.Div(
                                    dcc.Loading(
                                        id='my-loading-10',
                                        type='circle',
                                        children= dt.DataTable(
                                            id="table_patterns",
                                            style_table={'width': '100%',
                                                         "border-radius": "10px",
                                                         'marginTop': 0,},
                                            style_cell={
                                                'textAlign': 'center',
                                                "white_space": "normal",
                                                "backgroundColor": colors["background"],
                                                "color": "white",
                                                "font_size": "14px",
                                                'font-family':'montserrat',
                                                'font-weight': "lighter",
                                            },
                                            style_data={"border": "#4d4d4d"},
                                            style_header={
                                                "backgroundColor": colors["background"],
                                                #"fontWeight": "regular",
                                                "border": "#4d4d4d",
                                                'border-bottom': '1px solid black',
                                                #'font-family': 'Lato',
                                            },
                                            editable=False,
                                            row_selectable='single',
                                            style_cell_conditional=[
                                                {"if": {"column_id": c}, "textAlign": "center"}
                                                for c in ["attribute", "value"]
                                            ],
                                            #["Ticker 1", "Ticker 2", "Start Date", "End Date", "Standard deviation", "Critical Value", "Executable", "Backtest"]
                                            columns=[    
                                                {'name': 'TICKER', 'id': 'ticker'},
                                                {'name': 'PATTERN', 'id': 'pattern'},
                                                {'name': 'MARKET', 'id': 'market'},
                                            ],
                                        ),
                                    ),
                                    style={
                                        "background-color": "#151519",
                                        "color": colors["text"],
                                        #"color": "white",
                                        "border-style": "none",
                                        "border-radius": "15px",
                                        "padding": "10px",
                                    },
                                ),
                                html.Br(),
                                html.Label(
                                    "Backtesting",
                                    style={
                                        "textAlign": "left",
                                        "color": colors["text"],
                                        "margin-left": "5px",
                                        "border-bottom": "1px solid white"
                                    },
                                ),
                                html.Br(),
                                html.Br(),
                                html.Label(
                                    "Ticker",
                                    style={
                                        "textAlign": "left",
                                        "color": colors["text"],
                                        "margin": "0px 0px 10px 5px",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="ticker1",
                                    options=[
                                        {
                                            "label": str(ticker_list[i]),
                                            "value": str(ticker_list[i]),
                                        }
                                        for i in range(len(ticker_list))
                                    ],
                                    value=["TSLA","GOOGL","F","GE","AAL","DIS","DAL","AAPL","MSFT","CCL","GPRO","ACB","PLUG","AMZN"],
                                    multi=False,
                                    style={
                                        "background-color": "#151519",
                                        "color": colors["text"],
                                        "border-style": "none",
                                        "border-radius": "15px",
                                    },
                                ),
                                html.Br(),
                                html.Label(
                                    "Entry patterns",
                                    style={
                                        "textAlign": "left",
                                        "color": colors["text"],
                                        "margin": "0px 0px 10px 5px",
                                    },
                                ),
                                html.Br(),
                                dcc.Dropdown(
                                    id="entry-patterns-dropdown-backtesting",
                                    options=[
                                        {
                                            "label": str(patterns[i]),
                                            "value": str(patterns[i]),
                                        }
                                        for i in range(len(patterns))
                                    ],
                                    multi=True,
                                    style={
                                        "background-color": "#151519",
                                        "color": colors["text"],
                                        "border-style": "none",
                                        "border-radius": "15px",
                                    },
                                ),
                                html.Br(),
                                html.Label(
                                    "Exit patterns",
                                    style={
                                        "textAlign": "left",
                                        "color": colors["text"],
                                        "margin": "0px 0px 10px 5px",
                                    },
                                ),
                                html.Br(),
                                dcc.Dropdown(
                                    id="exit-patterns-dropdown-backtesting",
                                    options=[
                                        {
                                            "label": str(patterns[i]),
                                            "value": str(patterns[i]),
                                        }
                                        for i in range(len(patterns))
                                    ],
                                    multi=True,
                                    style={
                                        "background-color": "#151519",
                                        "color": colors["text"],
                                        #"color": "white",
                                        "border-style": "none",
                                        "border-radius": "15px",
                                    },
                                ),
                                html.Br(),
                                dbc.Row(
                                    [
                                    dbc.Col(
                                        [  
                                        html.Label(
                                            "Period",
                                            style={
                                                "textAlign": "left",
                                                "color": colors["text"],
                                                "margin": "0px 0px 10px 5px",
                                            },
                                        ),
                                        html.Br(),
                                        html.Div(
                                            [
                                                dcc.Input(
                                                    id="date",
                                                    type='number', 
                                                    min=1, 
                                                    max=10, 
                                                    value=10,
                                                    step=1,
                                                    style={
                                                        "background-color": "#151519",
                                                        "color": colors["text"],
                                                        "border-style": "none",
                                                        "border-radius": "15px",
                                                        "padding": "5px 5px 5px 10px",
                                                    },
                                                ),
                                                html.Label(
                                                    "years",
                                                    style={
                                                        "margin": "2px 0px 0px 10px",
                                                        "text-align": "center",
                                                        }
                                                ),
                                            ],
                                            style={'display': 'flex',}
                                        ),
                                        ],
                                        width=3,
                                    ),
                                    html.Br(),
                                    dbc.Col(
                                        [
                                        html.Label(
                                            "Direction",
                                            style={
                                                "textAlign": "left",
                                                "color": colors["text"],
                                                "margin": "0px 0px 10px 5px",
                                            },
                                        ),
                                        html.Br(),
                                        dcc.Dropdown(
                                            id="direction",
                                            options=[
                                                {"label": 'LongOnly',"value": 'LongOnly',},
                                                {"label": 'ShortOnly',"value": 'ShortOnly'},
                                                {"label": 'Both',"value": 'Both',},
                                            ],
                                            value='LongOnly',
                                            multi=False,
                                            style={
                                                "background-color": "#151519",
                                                "color": colors["text"],
                                                "border-style": "none",
                                                "border-radius": "15px",
                                            },
                                        ),
                                        ],
                                        style={"padding-left": "30px"},
                                        width=6,
                                    ),
                                    ]
                                ),
                                html.Br(),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.Label(
                                                    "Initial Cash",
                                                    style={
                                                        "textAlign": "left",
                                                        "color": colors["text"],
                                                        "margin": "0px 0px 10px 5px",
                                                        "width": "100%", 
                                                    },
                                                ),
                                                html.Br(),
                                                dcc.Input(
                                                    id="initial_cash",
                                                    type='number', 
                                                    max=100000000,
                                                    value=1000,
                                                    step=50,
                                                    style={
                                                        "background-color": "#151519",
                                                        "color": colors["text"],
                                                        #"color": "white",
                                                        "border-style": "none",
                                                        "border-radius": "15px",
                                                        "padding": "5px 5px 5px 10px",
                                                    },
                                                ),
                                            ],
                                            width=5,
                                        ),
                                        dbc.Col(
                                            [
                                                html.Label(
                                                    "Fees",
                                                    style={
                                                        "textAlign": "left",
                                                        "color": colors["text"],
                                                        "margin": "0px 0px 10px 5px",
                                                        "width": "100%", 
                                                    },
                                                ),
                                                html.Br(),
                                                dcc.Input(
                                                    id="fees",
                                                    type='number', 
                                                    min=0, 
                                                    max=1,
                                                    value=0.01,
                                                    step=0.01,
                                                    style={
                                                        "background-color": "#151519",
                                                        "color": colors["text"],
                                                        #"color": "white",
                                                        "border-style": "none",
                                                        "border-radius": "15px",
                                                        "padding": "5px 5px 5px 10px",
                                                    },   
                                                ),
                                            ],
                                            style={"padding-left": "30px"},
                                            width=3,
                                        ),
                                        dbc.Col(
                                            [
                                                html.Label(
                                                    "Slippage",
                                                    style={
                                                        "textAlign": "left",
                                                        "color": colors["text"],
                                                        "margin": "0px 0px 10px 5px",
                                                        "width": "100%", 
                                                    },
                                                ),
                                                dcc.Input(
                                                    id="slippage",
                                                    type='number', 
                                                    min=0, 
                                                    max=0.1,
                                                    value=0.005,
                                                    step=0.001,
                                                    style={
                                                        "background-color": "#151519",
                                                        "color": colors["text"],
                                                        #"color": "white",
                                                        "border-style": "none",
                                                        "border-radius": "15px",
                                                        "padding": "5px 5px 5px 10px",
                                                    },
                                                ),
                                             ],
                                            width=3,
                                        ),  
                                    ]
                                ),
                                html.Br(),
                                dcc.Checklist(
                                    id='my-checkbox',
                                    options=[
                                        {'label': 'Export Excel file', 'value': 'Checked'},
                                    ],
                                    value=[],
                                    inputStyle={"margin": "10px 5px 0 0",},
                                    style={'font-size': '16px', 'color': 'white', 'margin': '0 0 10px 5px'}
                                ),
                                
                            ],
                            width=4
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    dcc.Loading(
                                        id='my-loading-1',
                                        type='circle',
                                        children=dcc.Graph(
                                            id="graph",
                                            figure={
                                                'layout': go.Layout(
                                                    plot_bgcolor=colors["background"],
                                                    paper_bgcolor=colors["background"],
                                                )
                                            },
                                        ),
                                    ),
                                    style={'border-radius':'10px', "background-color": "#151519", 'padding': '30px'},
                                ),
                                html.Br(),
                                html.Div(
                                    dcc.Loading(
                                        id='my-loading-2',
                                        type='circle',
                                        children=dcc.Graph(
                                            id="graph_return",
                                           figure={
                                               'layout': go.Layout(
                                                   plot_bgcolor=colors["background"],
                                                   paper_bgcolor=colors["background"],
                                               )
                                           },
                                            style={'border-radius':'15px', 'width': '100%', 'margin-left': '10px'},
                                        ),
                                        style={"width": "100%"},  
                                    ),
                                    style={'border-radius':'10px', "background-color": "#151519", "width": "100%", 'padding': '30px'},
                                ),
                                html.Br(),
                                html.Div(
                                    dcc.Loading(
                                        id='my-loading-3',
                                        type='circle',
                                            children=dcc.Graph(
                                            id="graph_orders",
                                           figure={
                                               'layout': go.Layout(
                                                   plot_bgcolor=colors["background"],
                                                   paper_bgcolor=colors["background"],
                                               )
                                           },
                                            style={'border-radius':'15px', 'width': '100%', 'margin-left': '10px'},
                                        ),
                                       style={"width": "100%"},     
                                    ),
                                    style={'border-radius':'10px', "background-color": "#151519", "width": "100%", 'padding': '30px'},
                                ),
                                html.Br(),
                            ],
                            width=8
                        ),
                    ],
                    style={
                        "padding": "0px",
                    },
                )
            ],
            style={
                "padding": "40px",
                'font-family':'montserrat',
                'font-weight': "lighter",
            },
            
        ),
        #html.Br(),
    ],
)

@app.callback(
    # output
     [Output("table_patterns", "data"),
      Output('table_patterns', 'selected_rows'),],
    # input
    [Input("ticker", "value"),]
)
def table_genrator(ticker): #btn_price, btn_lr, btn_cointegration, btn_chart):

    ctx = dash.callback_context

    if not ctx.triggered or len(ticker) == 0:
        return dash.no_update, dash.no_update
    
    df = get_candlesticks_patterns(ticker)

    if len(df) == 0:
        return dash.no_update, dash.no_update
    
    df = df.to_dict("records")
    
    return df, [0]
 
@app.callback(
    # output
    #[Output("graph", "figure"),
     [Output("entry-patterns-dropdown-backtesting", "value"),
      Output("exit-patterns-dropdown-backtesting", "value"),
      Output("ticker1", "value"),
      Output("direction", "value"),],
    # input
    Input('table_patterns', 'selected_rows'),
    State('table_patterns', 'data'), 
)
def graph_genrator(selected_rows, data):
 
    ctx = dash.callback_context

    if not ctx.triggered:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update
    
    row_index = selected_rows[0]
    row = data[row_index]
    
    ticker = row['ticker']
    pattern = 'CDL' + str(row['pattern'])
    market  = row['market']
    
    direction = 'LongOnly' if market == 'BULL' else 'ShortOnly'
    
    if market == 'BULL':
        return [pattern], exit_patterns, ticker, direction
    else:
        return [pattern], entry_patterns, ticker, direction

@app.callback(
    #Output
    [Output("graph", "figure"),
     Output("graph_return", "figure"),
     Output("graph_orders", "figure"),
     Output("download-file", "data"),
     ],
    #Input
    [
     Input("ticker1", "value"),
     Input("entry-patterns-dropdown-backtesting", "value"),
     Input("exit-patterns-dropdown-backtesting", "value"),
     Input('date', 'value'),
     Input('fees', 'value'),
     Input('slippage', 'value'),
     Input('direction', 'value'),
     Input('initial_cash', 'value'),
     ],
    State('my-checkbox', 'value'),
    prevent_initial_call=True,
)
def backtester_graphs(ticker, entries, exits, date, fees, slippage, direction, initial_cash, value):#, date, train, test, fees, slippage, stoploss, value):
    
    ctx = dash.callback_context

    if not ctx.triggered or any(not var for var in [ticker, entries, exits, date, fees, slippage, direction, initial_cash]):
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    new_layout ={
        "width": 820,
        #"border-radius": "10px",
        "showlegend": True,
        "plot_bgcolor": colors["background"],
        "paper_bgcolor": colors["background"],
        "font": {"size": 12, "family": "Montserrat", "color": "#5E5E5E"},
        "margin": {"l": 0, "r": 0, "t": 0, "b": 0},

    }  
    
    start_date = datetime.date.today() - timedelta(days=date * 365)
    end_date = datetime.date.today()
    
    try:
        df = yf.download(ticker, start=start_date)
    except Exception as e:
        print(f"Error occurred while downloading {ticker}: {e}")
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update
    
    pattern_entries = [[0]*len(df)]
    for pattern in entries:
        pattern_values = getattr(talib, pattern)(df['Open'], df['High'], df['Low'], df['Close'])
        bull_entries = pattern_values > 0
        bear_entries = pattern_values < 0
        pattern_values[bull_entries] = pattern[3:] + '_BULL'
        pattern_values[bear_entries] = pattern[3:] + '_BEAR'
        pattern_entries = np.where(pattern_values != 0, pattern_values, pattern_entries)
    annotations = []
    for i, txt in enumerate(pattern_values):
        if txt != 0:
            annotations.append(dict(x=df.index[i], y=df['High'][i], text=txt, showarrow=False, font=dict(color='#1B62A5',size=8), textangle=-90))

    
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=list(df.index),
                open=list(df['Open']),
                high=list(df['High']),
                low=list(df['Low']),
                close=list(df['Close']),
                name="Candlestick",
            )
        ],
        layout=go.Layout(
            annotations=annotations,
            xaxis=dict(
                visible=True,
                linecolor='#5E5E5E',
                linewidth=0.5,
                showgrid=False,
                tickfont=dict(
                    family='Montserrat',
                    color='#5E5E5E',
                    size=12,
                    #weight='bold'
                )
            ), 
            yaxis=dict(
                visible=True,
                linecolor='#5E5E5E',
                linewidth=0.5,
                showgrid=True,
                gridcolor='#5E5E5E',
                gridwidth=0.5,
                tickfont=dict(
                    family='Montserrat',
                    color='#5E5E5E',
                    size=12,
                    #weight='bold'
                )
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            #xaxis_rangeslider_visible=False,
            margin_t=0,
            margin_r=0,
            margin_b=0,
            margin_l=0,
        )
    )
    
    position, df_position, positions = backtesting(df, entries, exits, fees, slippage, direction, initial_cash)
    
    fig1 = position.value().vbt.plot()
    fig1.update_layout(new_layout, xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),yaxis=dict(gridcolor='rgba(255,255,255,0.1)'))
    close = df['Close']
    returns = close.pct_change()
    cumulative_returns = (1 + returns).cumprod() * 1000
    fig1 = fig1.add_scatter(x=cumulative_returns.index, y=cumulative_returns, alignmentgroup='Buy & Hold', mode='lines', marker=dict(color='#5E5E5E', line=dict(color='#5E5E5E')), name='Buy & Hold')
    
    fig2 = position.orders.plots()
    fig2.update_layout(new_layout, xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),yaxis=dict(gridcolor='rgba(255,255,255,0.1)'))

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter('new_excel_file.xlsx', engine='xlsxwriter')
    
    # Write each dataframe to a different worksheet.
    df_position.to_excel(writer, sheet_name='returns')
    positions.to_excel(writer, sheet_name='positions')
    
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

    if value:    
        return fig, fig1, fig2, dcc.send_file('new_excel_file.xlsx')
    else:
        return fig, fig1, fig2, dash.no_update


@app.callback(
    [Output("index-dropdown", 'options'),
     Output("ticker1", 'options'),
     Output("category-dropdown", 'options'),
     Output("ticker1", "value", allow_duplicate=True),
     Output("ticker", "options", allow_duplicate=True)
     ],
    [Input('country-dropdown', 'value'),
    Input('index-dropdown', 'value'),
    Input('category-dropdown', 'value'),],
)
def update_output(country, index, category):

    ctx = dash.callback_context
    
    if not ctx.triggered:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    else:
        changed_dropdown_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if changed_dropdown_id == 'country-dropdown':
            index_list = np.sort(df[df['Country'] == country]['Exchange'].unique())
            ticker_list = np.sort(df[df['Country'] == country]['Ticker'].unique())    
            category_list = np.sort(df[df['Country'] == country].dropna()['Category Name'].unique())   
            return index_list, ticker_list, category_list, None, ticker_list
        elif changed_dropdown_id == 'index-dropdown':
            ticker_list = np.sort(df[df['Exchange'].isin(index)]['Ticker'].unique())    
            category_list = np.sort(df[df['Exchange'].isin(index)].dropna()['Category Name'].unique())    
            return dash.no_update, ticker_list,  category_list, None,  ticker_list
        elif changed_dropdown_id == 'category-dropdown':  
            ticker_list = np.sort(df.loc[(df['Exchange'].isin(index)) & (df['Category Name'] == category)]['Ticker'].unique())  
            return dash.no_update, ticker_list, dash.no_update, None, ticker_list
    
@app.callback(
    [Output("ticker", "value", allow_duplicate=True), Output("ticker", "options"), Output('add-from-index', 'n_clicks'), Output('add-from-category', 'n_clicks')],
    [Input('add-from-index', 'n_clicks'),
    Input('add-from-category', 'n_clicks'),],
    [State('country-dropdown', 'value'),
    State('index-dropdown', 'value'),
    State('category-dropdown', 'value'),]
)
def add_tickers(n_click_index, n_click_category, country, index, category):
    
    if n_click_index is not None and n_click_index > 0:
        if len(df[df['Exchange'].isin(index)]['Ticker']) > 200:
            tickers = np.random.choice(df[df['Exchange'].isin(index)]['Ticker'].unique(), size=200, replace=False)
        else:
            tickers = np.sort(df[df['Exchange'].isin(index)]['Ticker'].unique())
        return tickers, tickers, 0, 0
    
    if n_click_category is not None and n_click_category > 0:
        tickers = np.sort(df.loc[(df['Exchange'].isin(index)) & (df['Category Name'] == category)]['Ticker'].unique())
        return tickers, tickers, 0, 0
    
    return dash.no_update, dash.no_update, 0, 0


if __name__ == "__main__":
    app.run_server(debug=True)

    
    