import pandas as pd
from ta.trend import SMAIndicator

def should_trade(exchange, symbol):
    ohlcv = exchange.fetch_ohlcv(symbol, '1m', limit=50)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    sma_short = SMAIndicator(df['close'], window=10).sma_indicator()
    sma_long = SMAIndicator(df['close'], window=30).sma_indicator()

    if sma_short.iloc[-1] > sma_long.iloc[-1]:
        return 'buy'
    elif sma_short.iloc[-1] < sma_long.iloc[-1]:
        return 'sell'
    return None
