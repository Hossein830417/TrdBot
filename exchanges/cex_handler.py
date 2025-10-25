import ccxt

class CEXHandler:
    def __init__(self, exchange_name, api_key, secret):
        self.exchange = getattr(ccxt, exchange_name)({
            'apiKey': api_key,
            'secret': secret,
            'enableRateLimit': True
        })

    def fetch_price(self, symbol):
        return self.exchange.fetch_ticker(symbol)['last']

    def place_order(self, symbol, side, amount):
        return self.exchange.create_market_order(symbol, side, amount)
