import ccxt
import pandas as pd
from ta.momentum import RSIIndicator

def should_trade(exchange, symbol):
    ohlcv = exchange.fetch_ohlcv(symbol, '1m', limit=14)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    rsi = RSIIndicator(df['close'], window=14).rsi()

    current_rsi = rsi.iloc[-1]
    if current_rsi < 30:
        return 'buy'
    elif current_rsi > 70:
        return 'sell'
    return None
