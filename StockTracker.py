import requests
import pandas as pd
from math import pi
from bokeh.plotting import figure, show

api_key = ""
try:
    ticker = input("Enter the symbol of company listed in S&P 500 index:")
    url_data = f'https://api.stockdata.org/v1/data/eod?symbols={ticker}&api_token={api_key}'
    response = requests.get(url_data).json()

    col_name = ['date', 'open', 'low', 'high', 'close', 'volume']
    daily_price = pd.DataFrame(response['data'])[0:100]
    daily_price['date'] = daily_price['date'].str[:10]
    daily_price['date'] = pd.to_datetime(daily_price['date'])
    daily_price.columns = col_name

    inc = daily_price.close > daily_price.open
    dec = daily_price.open > daily_price.close
    w = 12*60*60*1000

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    p = figure(x_axis_type="datetime", tools=TOOLS, width=1000,
               title=f'{ticker} last 100 end-of-day quotes')
    p.xaxis.major_label_orientation = pi/4
    p.grid.grid_line_alpha = 0.3

    p.segment(daily_price.date, daily_price.high, daily_price.date, daily_price.low, color="black")
    p.vbar(daily_price.date[inc], w, daily_price.open[inc], daily_price.close[inc],
           fill_color="#35B778", line_color="black")
    p.vbar(daily_price.date[dec], w, daily_price.open[dec], daily_price.close[dec],
           fill_color="#F2583E", line_color="black")

    show(p)

except KeyError or AttributeError:
    print('Wrong company symbol!')
