import ccxt
from datetime import datetime
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketDataCollector:
    def __init__(self, exchange_name='binance'):
        self.exchange = getattr(ccxt, exchange_name)()
    
    def get_ticker(self, symbol):
        """Fetches the latest price and volume for a given symbol."""
        try:
            data = self.exchange.fetch_ticker(symbol)
            return {
                'symbol': symbol,
                'bid': data['bid'],
                'ask': data['ask'],
                'high': data['high'],
                'low': data['low'],
                'volume': data['volume'],
                'timestamp': datetime.now().isoformat()
            }
        except ccxt.BaseError as e:
            logger.error(f"Failed to fetch ticker: {e}")
            return None
    
    def get_ohlc(self, symbol, interval='1h', limit=24):
        """Fetches OHLCV data for a given symbol."""
        try:
            ohlc_data = self.exchange.fetch_ohlcv(symbol, timeframe=interval, limit=limit)
            return [{
                'symbol': symbol,
                'open': entry[0],
                'high': entry[1],
                'low': entry[2],
                'close': entry[3],
                'volume': entry[4],
                'timestamp': self.exchange.iso8601(entry[5])
            } for entry in ohlc_data]
        except ccxt.BaseError as e:
            logger.error(f"Failed to fetch OHLCV: {e}")
            return None

if __name__ == '__main__':
    collector = MarketDataCollector()
    symbol = 'BTC/USDT'
    print(collector.get_ticker(symbol))
    print(collector.get_ohlc(symbol))