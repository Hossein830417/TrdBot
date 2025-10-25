import pandas as pd
from ta.volatility import BollingerBands

def should_trade(exchange, symbol):
    ohlcv = exchange.fetch_ohlcv(symbol, '1m', limit=20)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    bb = BollingerBands(df['close'], window=20, window_dev=2)

    current_close = df['close'].iloc[-1]
    bb_high = bb.bollinger_hband().iloc[-1]
    bb_low = bb.bollinger_lband().iloc[-1]

    if current_close < bb_low:
        return 'buy'
    elif current_close > bb_high:
        return 'sell'
    return None
