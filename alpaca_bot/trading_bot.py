#!/usr/bin/env python3
"""
Alpaca Paper Trading Bot
A safe paper trading bot that connects to Alpaca's API and executes simple trades.
Author: Your Name
Date: 2024
"""

import os
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame

# ==================== CONFIGURATION ====================

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/trading.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ==================== ALPACA API CLASS ====================

class AlpacaPaperTrader:
    """
    A class to handle paper trading operations with Alpaca API
    """

    def __init__(self):
        """
        Initialize the Alpaca API connection using environment variables
        """
        try:
            # Get API credentials from environment variables
            self.api_key = os.getenv('APCA_API_KEY_ID')
            self.api_secret = os.getenv('APCA_API_SECRET_KEY')
            self.base_url = os.getenv('APCA_API_BASE_URL')

            # Validate that all required environment variables are present
            if not all([self.api_key, self.api_secret, self.base_url]):
                raise ValueError("Missing required environment variables. Please check your .env file.")

            # Initialize the Alpaca API client
            self.api = tradeapi.REST(
                key_id=self.api_key,
                secret_key=self.api_secret,
                base_url=self.base_url,
                api_version='v2'
            )

            logger.info("Successfully connected to Alpaca API")

        except Exception as e:
            logger.error(f"Failed to initialize Alpaca API: {str(e)}")
            raise

    def get_account_info(self) -> Dict:
        """
        Retrieve and display account information

        Returns:
            Dict containing account status, buying power, and cash balance
        """
        try:
            account = self.api.get_account()

            account_info = {
                'status': account.status,
                'buying_power': float(account.buying_power),
                'cash': float(account.cash),
                'portfolio_value': float(account.portfolio_value),
                'day_trading_buying_power': float(account.daytrading_buying_power),
                'pattern_day_trader': account.pattern_day_trader
            }

            # Print formatted account information
            print("\n" + "="*50)
            print("ACCOUNT INFORMATION")
            print("="*50)
            print(f"Account Status: {account_info['status']}")
            print(f"Buying Power: ${account_info['buying_power']:,.2f}")
            print(f"Cash Balance: ${account_info['cash']:,.2f}")
            print(f"Portfolio Value: ${account_info['portfolio_value']:,.2f}")
            print(f"Pattern Day Trader: {account_info['pattern_day_trader']}")
            print("="*50 + "\n")

            logger.info(f"Retrieved account info: Status={account_info['status']}, "
                       f"Buying Power=${account_info['buying_power']:,.2f}")

            return account_info

        except Exception as e:
            logger.error(f"Failed to get account information: {str(e)}")
            raise

    def place_market_order(self, symbol: str, qty: int, side: str) -> Optional[Dict]:
        """
        Place a market order (buy or sell)

        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            qty: Number of shares to trade
            side: 'buy' or 'sell'

        Returns:
            Dict containing order details or None if failed
        """
        try:
            # Validate inputs
            if side.lower() not in ['buy', 'sell']:
                raise ValueError("Side must be 'buy' or 'sell'")

            # Submit the market order
            order = self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side=side.lower(),
                type='market',
                time_in_force='day'  # Day order - expires at market close
            )

            order_info = {
                'id': order.id,
                'symbol': order.symbol,
                'qty': order.qty,
                'side': order.side,
                'type': order.order_type,
                'status': order.status,
                'submitted_at': order.submitted_at
            }

            print(f"\n✅ Market Order Placed:")
            print(f"   Symbol: {symbol}")
            print(f"   Side: {side.upper()}")
            print(f"   Quantity: {qty}")
            print(f"   Order ID: {order.id}")
            print(f"   Status: {order.status}\n")

            logger.info(f"Market order placed: {side.upper()} {qty} shares of {symbol}, "
                       f"Order ID: {order.id}")

            return order_info

        except Exception as e:
            logger.error(f"Failed to place market order: {str(e)}")
            print(f"❌ Error placing order: {str(e)}")
            return None

    def get_positions(self) -> List[Dict]:
        """
        Check and display current positions (holdings)

        Returns:
            List of position dictionaries
        """
        try:
            positions = self.api.list_positions()

            if not positions:
                print("\n📊 No open positions")
                logger.info("No open positions found")
                return []

            print("\n" + "="*50)
            print("CURRENT POSITIONS")
            print("="*50)

            position_list = []
            for position in positions:
                pos_info = {
                    'symbol': position.symbol,
                    'qty': int(position.qty),
                    'avg_entry_price': float(position.avg_entry_price),
                    'current_price': float(position.current_price),
                    'market_value': float(position.market_value),
                    'unrealized_pl': float(position.unrealized_pl),
                    'unrealized_plpc': float(position.unrealized_plpc) * 100  # Convert to percentage
                }

                position_list.append(pos_info)

                print(f"\nSymbol: {pos_info['symbol']}")
                print(f"  Quantity: {pos_info['qty']}")
                print(f"  Avg Entry Price: ${pos_info['avg_entry_price']:.2f}")
                print(f"  Current Price: ${pos_info['current_price']:.2f}")
                print(f"  Market Value: ${pos_info['market_value']:.2f}")
                print(f"  Unrealized P/L: ${pos_info['unrealized_pl']:.2f} "
                      f"({pos_info['unrealized_plpc']:.2f}%)")

            print("="*50 + "\n")

            logger.info(f"Retrieved {len(position_list)} open positions")
            return position_list

        except Exception as e:
            logger.error(f"Failed to get positions: {str(e)}")
            print(f"❌ Error getting positions: {str(e)}")
            return []

    def get_recent_orders(self, limit: int = 5) -> List[Dict]:
        """
        Retrieve and display recent orders

        Args:
            limit: Number of recent orders to retrieve

        Returns:
            List of order dictionaries
        """
        try:
            # Get recent orders (both open and closed)
            orders = self.api.list_orders(
                status='all',  # Get all orders regardless of status
                limit=limit,
                direction='desc'  # Most recent first
            )

            if not orders:
                print("\n📋 No orders found")
                logger.info("No orders found")
                return []

            print("\n" + "="*50)
            print(f"LAST {limit} ORDERS")
            print("="*50)

            order_list = []
            for order in orders:
                order_info = {
                    'symbol': order.symbol,
                    'side': order.side,
                    'qty': order.qty,
                    'status': order.status,
                    'type': order.order_type,
                    'submitted_at': order.submitted_at,
                    'filled_at': order.filled_at,
                    'filled_qty': order.filled_qty if order.filled_qty else 0
                }

                order_list.append(order_info)

                print(f"\nSymbol: {order_info['symbol']}")
                print(f"  Side: {order_info['side'].upper()}")
                print(f"  Quantity: {order_info['qty']}")
                print(f"  Status: {order_info['status']}")
                print(f"  Type: {order_info['type']}")
                print(f"  Submitted: {order_info['submitted_at']}")
                if order_info['filled_at']:
                    print(f"  Filled: {order_info['filled_at']}")

            print("="*50 + "\n")

            logger.info(f"Retrieved {len(order_list)} recent orders")
            return order_list

        except Exception as e:
            logger.error(f"Failed to get recent orders: {str(e)}")
            print(f"❌ Error getting orders: {str(e)}")
            return []

    def check_market_status(self) -> bool:
        """
        Check if the market is currently open

        Returns:
            True if market is open, False otherwise
        """
        try:
            clock = self.api.get_clock()

            print(f"\n🕐 Market Status: {'OPEN' if clock.is_open else 'CLOSED'}")
            print(f"   Current Time: {clock.timestamp}")
            print(f"   Next Open: {clock.next_open}")
            print(f"   Next Close: {clock.next_close}\n")

            logger.info(f"Market is {'open' if clock.is_open else 'closed'}")

            return clock.is_open

        except Exception as e:
            logger.error(f"Failed to check market status: {str(e)}")
            return False

# ==================== MAIN EXECUTION ====================

def main():
    """
    Main function to execute the trading bot workflow
    """
    try:
        print("\n" + "="*60)
        print(" ALPACA PAPER TRADING BOT - STARTING ".center(60, "="))
        print("="*60 + "\n")

        # Initialize the trader
        trader = AlpacaPaperTrader()

        # Step 1: Check market status
        print("\n📌 Step 1: Checking market status...")
        is_open = trader.check_market_status()

        # Step 2: Get and display account information
        print("\n📌 Step 2: Getting account information...")
        account_info = trader.get_account_info()

        # Step 3: Check current positions
        print("\n📌 Step 3: Checking current positions...")
        positions = trader.get_positions()

        # Step 4: Place a market buy order for AAPL
        print("\n📌 Step 4: Placing BUY order for AAPL...")
        buy_order = trader.place_market_order(
            symbol='AAPL',
            qty=1,
            side='buy'
        )

        if buy_order:
            # Step 5: Wait 60 seconds
            print("\n⏳ Waiting 60 seconds before selling...")
            for i in range(60, 0, -10):
                print(f"   {i} seconds remaining...")
                time.sleep(10)

            # Step 6: Place a market sell order for AAPL
            print("\n📌 Step 6: Placing SELL order for AAPL...")
            sell_order = trader.place_market_order(
                symbol='AAPL',
                qty=1,
                side='sell'
            )
        else:
            print("\n⚠️ Buy order failed, skipping sell order")
            logger.warning("Buy order failed, skipping sell order")

        # Step 7: Display recent orders
        print("\n📌 Step 7: Getting recent order history...")
        recent_orders = trader.get_recent_orders(limit=5)

        # Step 8: Final position check
        print("\n📌 Step 8: Final position check...")
        final_positions = trader.get_positions()

        # Step 9: Final account status
        print("\n📌 Step 9: Final account status...")
        final_account = trader.get_account_info()

        print("\n" + "="*60)
        print(" TRADING BOT EXECUTION COMPLETED ".center(60, "="))
        print("="*60 + "\n")

        logger.info("Trading bot execution completed successfully")

    except Exception as e:
        logger.error(f"Fatal error in main execution: {str(e)}")
        print(f"\n❌ Fatal Error: {str(e)}")
        raise

# ==================== ENTRY POINT ====================

if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)

    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Trading bot stopped by user")
        logger.info("Trading bot stopped by user")
    except Exception as e:
        print(f"\n\n❌ Trading bot crashed: {str(e)}")
        logger.error(f"Trading bot crashed: {str(e)}")
        exit(1)