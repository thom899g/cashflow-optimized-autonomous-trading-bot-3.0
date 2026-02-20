import ccxt
from typing import Dict, Any

class ExecutionEngine:
    def __init__(self, exchange):
        self.exchange = exchange
    
    def execute_order(self, symbol: str, side: str, amount: float) -> Dict[str, Any]:
        """Executes an order on the exchange."""
        try:
            order = self.exchange.create_order(symbol=symbol, side=side, type='market', quantity=amount)
            return {
                'order_id': order['id'],
                'symbol': symbol,
                'side': side,
                'amount': amount,
                'status': 'success'
            }
        except ccxt.BaseError as e:
            return {
                'error': str(e),
                'status': 'failed'
            }

    def get_order_status(self, order_id: str) -> Dict[str, Any]:
        """Fetches the status of a previously placed order."""
        try:
            order = self.exchange.fetch_order(order_id)
            return {
                'order_id': order['id'],
                'symbol': order['symbol'],
                'side': order['side'],
                'amount': order['quantity'],
                'status': order['status']
            }
        except ccxt.BaseError as e:
            return {'error': str(e)}

if __name__ == '__main__':
    exchange = ccxt.binance()
    engine = ExecutionEngine(exchange)
    print(engine.execute_order('BTC/USDT', 'buy', 0.1))