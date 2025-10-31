#!/usr/bin/env python3
"""
Alpaca Paper Trading Bot V2 - Using alpaca-py SDK
Compatible with Windows without C++ Build Tools
"""

import os
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Using the newer alpaca-py SDK
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, GetOrdersRequest
from alpaca.trading.enums import OrderSide, TimeInForce, QueryOrderStatus
from alpaca.common.exceptions import APIError

# ==================== CONFIGURATION ====================

# Load environment variables
load_dotenv()

# Set up logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/trading.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ==================== ALPACA TRADER CLASS ====================

class AlpacaTraderV2:
    """Modern Alpaca Paper Trading Bot using alpaca-py SDK"""

    def __init__(self):
        """Initialize the Alpaca trading client"""
        try:
            # Get credentials from environment
            api_key = os.getenv('APCA_API_KEY_ID')
            api_secret = os.getenv('APCA_API_SECRET_KEY')

            if not api_key or not api_secret:
                raise ValueError("Missing API credentials in .env file")

            # Initialize trading client (paper=True for paper trading)
            self.client = TradingClient(
                api_key=api_key,
                secret_key=api_secret,
                paper=True  # Always use paper trading
            )

            logger.info("Successfully connected to Alpaca Paper Trading API")
            print("✅ Connected to Alpaca Paper Trading API")

        except Exception as e:
            logger.error(f"Failed to initialize Alpaca client: {str(e)}")
            raise

    def get_account_info(self) -> Dict:
        """Get and display account information"""
        try:
            account = self.client.get_account()

            account_info = {
                'status': account.status,
                'buying_power': float(account.buying_power),
                'cash': float(account.cash),
                'portfolio_value': float(account.equity),
                'day_trading_buying_power': float(account.daytrading_buying_power) if account.daytrading_buying_power else 0,
                'pattern_day_trader': account.pattern_day_trader
            }

            print("\n" + "="*50)
            print("ACCOUNT INFORMATION")
            print("="*50)
            print(f"Account Status: {account_info['status']}")
            print(f"Buying Power: ${account_info['buying_power']:,.2f}")
            print(f"Cash Balance: ${account_info['cash']:,.2f}")
            print(f"Portfolio Value: ${account_info['portfolio_value']:,.2f}")
            print(f"Pattern Day Trader: {account_info['pattern_day_trader']}")
            print("="*50 + "\n")

            logger.info(f"Account: Buying Power=${account_info['buying_power']:,.2f}")
            return account_info

        except APIError as e:
            logger.error(f"API Error getting account: {e}")
            print(f"❌ API Error: {e}")
            return {}
        except Exception as e:
            logger.error(f"Failed to get account info: {str(e)}")
            print(f"❌ Error: {str(e)}")
            return {}

    def place_market_order(self, symbol: str, qty: int, side: str) -> Optional[Dict]:
        """Place a market order"""
        try:
            # Prepare order request
            order_side = OrderSide.BUY if side.lower() == 'buy' else OrderSide.SELL

            order_request = MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=order_side,
                time_in_force=TimeInForce.DAY
            )

            # Submit order
            order = self.client.submit_order(order_data=order_request)

            print(f"\n✅ Market Order Placed:")
            print(f"   Symbol: {symbol}")
            print(f"   Side: {side.upper()}")
            print(f"   Quantity: {qty}")
            print(f"   Order ID: {order.id}")
            print(f"   Status: {order.status}\n")

            logger.info(f"Order placed: {side.upper()} {qty} {symbol}, ID: {order.id}")

            return {
                'id': str(order.id),
                'symbol': order.symbol,
                'qty': order.qty,
                'side': str(order.side),
                'status': str(order.status)
            }

        except APIError as e:
            logger.error(f"API Error placing order: {e}")
            print(f"❌ API Error: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to place order: {str(e)}")
            print(f"❌ Error placing order: {str(e)}")
            return None

    def get_positions(self) -> List[Dict]:
        """Get current positions"""
        try:
            positions = self.client.get_all_positions()

            if not positions:
                print("📊 No open positions")
                return []

            print("\n" + "="*50)
            print("CURRENT POSITIONS")
            print("="*50)

            position_list = []
            for pos in positions:
                pos_info = {
                    'symbol': pos.symbol,
                    'qty': float(pos.qty),
                    'avg_entry_price': float(pos.avg_entry_price),
                    'current_price': float(pos.current_price) if pos.current_price else 0,
                    'market_value': float(pos.market_value),
                    'unrealized_pl': float(pos.unrealized_pl) if pos.unrealized_pl else 0
                }

                position_list.append(pos_info)

                print(f"\nSymbol: {pos_info['symbol']}")
                print(f"  Quantity: {pos_info['qty']}")
                print(f"  Avg Entry: ${pos_info['avg_entry_price']:.2f}")
                print(f"  Current: ${pos_info['current_price']:.2f}")
                print(f"  Market Value: ${pos_info['market_value']:.2f}")
                print(f"  Unrealized P/L: ${pos_info['unrealized_pl']:.2f}")

            print("="*50 + "\n")
            return position_list

        except Exception as e:
            logger.error(f"Failed to get positions: {str(e)}")
            return []

    def get_recent_orders(self, limit: int = 5) -> List[Dict]:
        """Get recent orders"""
        try:
            # Create request for all orders
            request = GetOrdersRequest(
                status=QueryOrderStatus.ALL,
                limit=limit,
                nested=False
            )

            orders = self.client.get_orders(filter=request)

            if not orders:
                print("📋 No orders found")
                return []

            print("\n" + "="*50)
            print(f"LAST {limit} ORDERS")
            print("="*50)

            order_list = []
            for order in orders:
                order_info = {
                    'symbol': order.symbol,
                    'side': str(order.side),
                    'qty': order.qty,
                    'status': str(order.status),
                    'submitted_at': str(order.submitted_at),
                    'filled_qty': order.filled_qty if order.filled_qty else 0
                }

                order_list.append(order_info)

                print(f"\nSymbol: {order_info['symbol']}")
                print(f"  Side: {order_info['side']}")
                print(f"  Quantity: {order_info['qty']}")
                print(f"  Status: {order_info['status']}")
                print(f"  Submitted: {order_info['submitted_at']}")

            print("="*50 + "\n")
            return order_list

        except Exception as e:
            logger.error(f"Failed to get orders: {str(e)}")
            return []

    def check_market_status(self) -> bool:
        """Check if market is open"""
        try:
            clock = self.client.get_clock()

            status = "OPEN" if clock.is_open else "CLOSED"
            print(f"\n🕐 Market Status: {status}")
            print(f"   Current Time: {clock.timestamp}")
            print(f"   Next Open: {clock.next_open}")
            print(f"   Next Close: {clock.next_close}\n")

            logger.info(f"Market is {status.lower()}")
            return clock.is_open

        except Exception as e:
            logger.error(f"Failed to check market status: {str(e)}")
            return False

# ==================== MAIN EXECUTION ====================

def main():
    """Main execution function"""
    try:
        print("\n" + "="*60)
        print(" ALPACA PAPER TRADING BOT V2 ".center(60, "="))
        print("="*60 + "\n")

        # Initialize trader
        trader = AlpacaTraderV2()

        # Step 1: Check market status
        print("📌 Step 1: Checking market status...")
        is_open = trader.check_market_status()

        if not is_open:
            print("⚠️  Market is closed. Orders will be queued for next session.")

        # Step 2: Get account information
        print("\n📌 Step 2: Getting account information...")
        account = trader.get_account_info()

        # Step 3: Check current positions
        print("\n📌 Step 3: Checking current positions...")
        positions = trader.get_positions()

        # Step 4: Place buy order
        print("\n📌 Step 4: Placing BUY order for AAPL...")
        buy_order = trader.place_market_order(
            symbol='AAPL',
            qty=1,
            side='buy'
        )

        if buy_order:
            # Step 5: Wait
            print("\n⏳ Waiting 60 seconds before selling...")
            for i in range(60, 0, -10):
                print(f"   {i} seconds remaining...")
                time.sleep(10)

            # Step 6: Place sell order
            print("\n📌 Step 6: Placing SELL order for AAPL...")
            sell_order = trader.place_market_order(
                symbol='AAPL',
                qty=1,
                side='sell'
            )
        else:
            print("⚠️  Buy order failed, skipping sell order")

        # Step 7: Get recent orders
        print("\n📌 Step 7: Getting recent order history...")
        recent_orders = trader.get_recent_orders(limit=5)

        # Step 8: Final check
        print("\n📌 Step 8: Final position check...")
        final_positions = trader.get_positions()

        print("\n" + "="*60)
        print(" EXECUTION COMPLETED ".center(60, "="))
        print("="*60 + "\n")

        logger.info("Trading bot execution completed")

    except KeyboardInterrupt:
        print("\n\n⚠️  Stopped by user")
        logger.info("Stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        print(f"\n❌ Fatal error: {str(e)}")
        raise

if __name__ == "__main__":
    main()