import json
import os
import time
from exchanges.cex_handler import CEXHandler
from strategies import rsi_strategy, ma_strategy, bb_strategy

# Load config
with open('config.json') as f:
    config = json.load(f)

# Initialize exchanges
exchanges = {}
for name, creds in config['exchanges'].items():
    exchanges[name] = CEXHandler(
        name,
        os.getenv(f"{name.upper()}_API_KEY"),
        os.getenv(f"{name.upper()}_SECRET")
    )

# Strategy mapping
STRATEGIES = {
    'rsi': rsi_strategy,
    'ma': ma_strategy,
    'bb': bb_strategy
}

def run_strategies(exchange_handler, symbol):
    signals = {}
    for strategy_name in config['strategies']:
        strategy = STRATEGIES[strategy_name]
        signal = strategy.should_trade(exchange_handler.exchange, symbol)
        signals[strategy_name] = signal
    return signals

def aggregate_signals(signals):
    buy_count = sum(1 for s in signals.values() if s == 'buy')
    sell_count = sum(1 for s in signals.values() if s == 'sell')
    
    if buy_count >= 2:
        return 'buy'
    elif sell_count >= 2:
        return 'sell'
    return None

def main():
    while True:
        for exchange_name, exchange_handler in exchanges.items():
            for symbol in config['symbols']:
                signals = run_strategies(exchange_handler, symbol)
                final_signal = aggregate_signals(signals)
                
                if final_signal:
                    print(f"[{exchange_name}] {symbol} -> {final_signal.upper()}")
                    try:
                        exchange_handler.place_order(symbol, final_signal, config['amount_per_trade'])
                    except Exception as e:
                        print(f"Error placing order: {e}")
        
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()
