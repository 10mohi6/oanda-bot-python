import os
import pytest
from oanda_bot import Bot
import time


@pytest.fixture(scope="module", autouse=True)
def scope_module():
    class MyBot(Bot):
        def strategy(self):
            rsi = self.rsi(period=10)
            ema = self.ema(period=20)
            self.buy_entry = (rsi < 30) & (self.df.C < ema)
            self.sell_entry = (rsi > 70) & (self.df.C > ema)
            self.sell_exit = ema > self.df.C
            self.buy_exit = ema < self.df.C
            self.units = 10000
            self.take_profit = 0
            self.stop_loss = 0

    yield MyBot(
        account_id=os.environ["OANDA_BOT_ID"],
        access_token=os.environ["OANDA_BOT_TOKEN"],
        environment="practice",
        instrument="USD_JPY",
        granularity="M1",
        trading_time=Bot.SUMMER_TIME,
        slack_webhook_url=os.environ["SLACK_WEBHOOK_URL"],
        line_notify_token=os.environ["LINE_NOTIFY_TOKEN"],
        discord_webhook_url=os.environ["DISCORD_WEBHOOK_URL"],
    )


@pytest.fixture(scope="function", autouse=True)
def bot(scope_module):
    time.sleep(0.5)
    yield scope_module


# @pytest.mark.skip
def test_error(bot):
    bot._error("oanda bot error test")


# @pytest.mark.skip
def test_backtest(bot):
    bot.backtest()


# @pytest.mark.skip
def test_report(bot):
    bot.report()
