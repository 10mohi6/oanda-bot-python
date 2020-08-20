# oanda-bot

[![PyPI](https://img.shields.io/pypi/v/oanda-bot)](https://pypi.org/project/oanda-bot/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/gh/10mohi6/oanda-bot-python/branch/master/graph/badge.svg)](https://codecov.io/gh/10mohi6/oanda-bot-python)
[![Build Status](https://travis-ci.com/10mohi6/oanda-bot-python.svg?branch=master)](https://travis-ci.com/10mohi6/oanda-bot-python)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/oanda-bot)](https://pypi.org/project/oanda-bot/)
[![Downloads](https://pepy.tech/badge/oanda-bot)](https://pepy.tech/project/oanda-bot)

oanda-bot is a python library for automated trading bot with oanda rest api on Python 3.6 and above.


## Installation

    $ pip install oanda-bot

## Usage

### basic run
```python
from oanda_bot import Bot

class MyBot(Bot):
    def strategy(self):
        fast_ma = self.sma(period=5)
        slow_ma = self.sma(period=25)
        # golden cross
        self.sell_exit = self.buy_entry = (fast_ma > slow_ma) & (
            fast_ma.shift() <= slow_ma.shift()
        )
        # dead cross
        self.buy_exit = self.sell_entry = (fast_ma < slow_ma) & (
            fast_ma.shift() >= slow_ma.shift()
        )

MyBot(
    account_id='<your practice account id>',
    access_token='<your practice access token>',
).run()
```

### basic backtest
```python
from oanda_bot import Bot

class MyBot(Bot):
    def strategy(self):
        fast_ma = self.sma(period=5)
        slow_ma = self.sma(period=25)
        # golden cross
        self.sell_exit = self.buy_entry = (fast_ma > slow_ma) & (
            fast_ma.shift() <= slow_ma.shift()
        )
        # dead cross
        self.buy_exit = self.sell_entry = (fast_ma < slow_ma) & (
            fast_ma.shift() >= slow_ma.shift()
        )

MyBot(
    account_id='<your practice account id>',
    access_token='<your practice access token>',
).backtest()
```

### basic report
```python
from oanda_bot import Bot

Bot(
    account_id='<your practice account id>',
    access_token='<your practice access token>',
).report()
```

### advanced run
```python
from oanda_bot import Bot

class MyBot(Bot):
    def strategy(self):
        rsi = self.rsi(period=10)
        ema = self.ema(period=20)
        lower = ema - (ema * 0.001)
        upper = ema + (ema * 0.001)
        self.buy_entry = (rsi < 30) & (self.df.C < lower)
        self.sell_entry = (rsi > 70) & (self.df.C > upper)
        self.sell_exit = ema > self.df.C
        self.buy_exit = ema < self.df.C
        self.units = 1000 # currency unit (default=10000)
        self.take_profit = 50 # take profit pips (default=0 take profit none)
        self.stop_loss = 20 # stop loss pips (default=0 stop loss none)

MyBot(
    account_id='<your practice account id>',
    access_token='<your practice access token>',
    # trading environment (default=practice)
    environment='practice',
    # trading currency (default=EUR_USD)
    instrument='USD_JPY',
    # 1 minute candlesticks (default=D)
    granularity='M1',
    # trading time (default=Bot.SUMMER_TIME)
    trading_time=Bot.WINTER_TIME,
    # Slack notification when an error occurs
    slack_webhook_url='<your slack webhook url>',
    # Line notification when an error occurs
    line_notify_token='<your line notify token>',
    # Discord notification when an error occurs
    discord_webhook_url='<your discord webhook url>',
).run()
```

### advanced backtest
```python
from oanda_bot import Bot

class MyBot(Bot):
    def strategy(self):
        rsi = self.rsi(period=10)
        ema = self.ema(period=20)
        lower = ema - (ema * 0.001)
        upper = ema + (ema * 0.001)
        self.buy_entry = (rsi < 30) & (self.df.C < lower)
        self.sell_entry = (rsi > 70) & (self.df.C > upper)
        self.sell_exit = ema > self.df.C
        self.buy_exit = ema < self.df.C
        self.units = 1000 # currency unit (default=10000)
        self.take_profit = 50 # take profit pips (default=0 take profit none)
        self.stop_loss = 20 # stop loss pips (default=0 stop loss none)

MyBot(
    account_id='<your practice account id>',
    access_token='<your practice access token>',
    instrument='USD_JPY',
    granularity='S15', # 15 second candlestick
).backtest(from_date="2020-7-7", to_date="2020-7-13", filename="backtest.png")
```
```python
total profit        3910.000
total trades         374.000
win rate              59.091
profit factor          1.115
maximum drawdown    4220.000
recovery factor        0.927
riskreward ratio       0.717
sharpe ratio           0.039
average return         9.787
stop loss              0.000
take profit            0.000
```
![backtest.png](https://raw.githubusercontent.com/10mohi6/oanda-bot-python/master/tests/backtest.png)

### advanced report
```python
from oanda_bot import Bot

Bot(
    account_id='<your practice account id>',
    access_token='<your practice access token>',
    instrument='USD_JPY',
    granularity='S15', # 15 second candlestick
).report(filename="report.png", days=-7) # from 7 days ago to now
```
```python
total profit        -4960.000
total trades          447.000
win rate               59.284
profit factor          -0.887
maximum drawdown    10541.637
recovery factor        -0.471
riskreward ratio       -0.609
sharpe ratio           -0.043
average return        -10.319
```
![report.png](https://raw.githubusercontent.com/10mohi6/oanda-bot-python/master/tests/report.png)

### live run
```python
from oanda_bot import Bot

class MyBot(Bot):
    def atr(self, *, period: int = 14, price: str = "C"):
        a = (self.df.H - self.df.L).abs()
        b = (self.df.H - self.df[price].shift()).abs()
        c = (self.df.L - self.df[price].shift()).abs()

        df = pd.concat([a, b, c], axis=1).max(axis=1)
        return df.ewm(span=period).mean()

    def strategy(self):
        rsi = self.rsi(period=10)
        ema = self.ema(period=20)
        atr = self.atr(period=20)
        lower = ema - atr
        upper = ema + atr
        self.buy_entry = (rsi < 30) & (self.df.C < lower)
        self.sell_entry = (rsi > 70) & (self.df.C > upper)
        self.sell_exit = ema > self.df.C
        self.buy_exit = ema < self.df.C
        self.units = 1000

MyBot(
    account_id='<your live account id>',
    access_token='<your live access token>',
    environment='live',
    instrument='EUR_GBP',
    granularity='H12', # 12 hour candlesticks
    trading_time=Bot.WINTER_TIME,
    slack_webhook_url='<your slack webhook url>',
).run()
```

## Supported indicators
- Simple Moving Average 'sma'
- Exponential Moving Average 'ema'
- Moving Average Convergence Divergence 'macd'
- Relative Strenght Index 'rsi'
- Bollinger Bands 'bbands'
- Market Momentum 'mom'
- Stochastic Oscillator 'stoch'
- Awesome Oscillator 'ao'


## Getting started

For help getting started with OANDA REST API, view our online [documentation](https://developer.oanda.com/rest-live-v20/introduction/).


## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request