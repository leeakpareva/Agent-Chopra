#!/usr/bin/env python3
"""
Extended Alpaca Paper Trading Bot with Additional Features
- Position checking
- Automatic scheduling
- Enhanced logging
"""

import os
import time
import logging
import schedule
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi

# Load environment variables
load_dotenv()

# Enhanced logging setup
def setup_logging():
    """Set up comprehensive logging configuration"""
    os.makedirs('logs', exist_ok=True)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File handler for all logs
    file_handler = logging.FileHandler('logs/trading.log')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # File handler for errors only
    error_handler = logging.FileHandler('logs/errors.log')
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_handler)
    root_logger.addHandler(console_handler)

    return logging.getLogger(__name__)

# Initialize logging
logger = setup_logging()

class ExtendedAlpacaTrader:
    """Extended Alpaca trader with additional features"""

    def __init__(self):
        """Initialize the extended trader"""
        try:
            self.api_key = os.getenv('APCA_API_KEY_ID')
            self.api_secret = os.getenv('APCA_API_SECRET_KEY')
            self.base_url = os.getenv('APCA_API_BASE_URL')

            if not all([self.api_key, self.api_secret, self.base_url]):
                raise ValueError("Missing API credentials in .env file")

            self.api = tradeapi.REST(
                key_id=self.api_key,
                secret_key=self.api_secret,
                base_url=self.base_url,
                api_version='v2'
            )

            logger.info("Extended Alpaca trader initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize trader: {str(e)}")
            raise

    def check_all_positions(self) -> Dict:
        """
        Check and analyze all current positions

        Returns:
            Detailed position analysis
        """
        try:
            positions = self.api.list_positions()
            account = self.api.get_account()

            if not positions:
                logger.info("No open positions found")
                return {
                    'total_positions': 0,
                    'total_market_value': 0,
                    'total_unrealized_pl': 0,
                    'positions': []
                }

            total_market_value = 0
            total_unrealized_pl = 0
            position_details = []

            print("\n" + "="*60)
            print(" CURRENT HOLDINGS ANALYSIS ".center(60, "="))
            print("="*60)

            for position in positions:
                market_value = float(position.market_value)
                unrealized_pl = float(position.unrealized_pl)
                unrealized_plpc = float(position.unrealized_plpc) * 100

                total_market_value += market_value
                total_unrealized_pl += unrealized_pl

                pos_detail = {
                    'symbol': position.symbol,
                    'quantity': int(position.qty),
                    'side': position.side,
                    'avg_entry_price': float(position.avg_entry_price),
                    'current_price': float(position.current_price),
                    'market_value': market_value,
                    'cost_basis': float(position.cost_basis),
                    'unrealized_pl': unrealized_pl,
                    'unrealized_plpc': unrealized_plpc,
                    'change_today': float(position.change_today) if position.change_today else 0
                }

                position_details.append(pos_detail)

                # Display position
                print(f"\n📊 {pos_detail['symbol']}:")
                print(f"   Quantity: {pos_detail['quantity']} shares")
                print(f"   Entry Price: ${pos_detail['avg_entry_price']:.2f}")
                print(f"   Current Price: ${pos_detail['current_price']:.2f}")
                print(f"   Market Value: ${pos_detail['market_value']:,.2f}")
                print(f"   Unrealized P/L: ${pos_detail['unrealized_pl']:,.2f} "
                      f"({'🟢' if pos_detail['unrealized_pl'] >= 0 else '🔴'} "
                      f"{abs(pos_detail['unrealized_plpc']):.2f}%)")

            # Portfolio summary
            portfolio_value = float(account.portfolio_value)
            positions_weight = (total_market_value / portfolio_value * 100) if portfolio_value > 0 else 0

            print("\n" + "-"*60)
            print(" PORTFOLIO SUMMARY ".center(60, "-"))
            print("-"*60)
            print(f"Total Positions: {len(positions)}")
            print(f"Total Market Value: ${total_market_value:,.2f}")
            print(f"Total Unrealized P/L: ${total_unrealized_pl:,.2f}")
            print(f"Portfolio Value: ${portfolio_value:,.2f}")
            print(f"Positions Weight: {positions_weight:.2f}%")
            print(f"Cash Available: ${float(account.cash):,.2f}")
            print("="*60 + "\n")

            result = {
                'total_positions': len(positions),
                'total_market_value': total_market_value,
                'total_unrealized_pl': total_unrealized_pl,
                'portfolio_value': portfolio_value,
                'positions_weight': positions_weight,
                'cash': float(account.cash),
                'positions': position_details
            }

            logger.info(f"Position check complete: {len(positions)} positions, "
                       f"Total value: ${total_market_value:,.2f}")

            return result

        except Exception as e:
            logger.error(f"Failed to check positions: {str(e)}")
            return {'error': str(e)}

    def run_trading_cycle(self):
        """
        Run a complete trading cycle
        This is the function that will be scheduled
        """
        try:
            logger.info("="*60)
            logger.info("Starting scheduled trading cycle")

            # Check if market is open
            clock = self.api.get_clock()
            if not clock.is_open:
                logger.info("Market is closed, skipping trading cycle")
                print(f"⏸️ Market is closed. Next open: {clock.next_open}")
                return

            # Get account info
            account = self.api.get_account()
            logger.info(f"Account status: {account.status}, "
                       f"Buying power: ${float(account.buying_power):,.2f}")

            # Check positions
            positions_data = self.check_all_positions()

            # Example: Simple trading logic (you can customize this)
            # Only trade if we have fewer than 3 positions
            if positions_data['total_positions'] < 3:
                # Example: Buy a small position in SPY
                try:
                    order = self.api.submit_order(
                        symbol='SPY',
                        qty=1,
                        side='buy',
                        type='market',
                        time_in_force='day'
                    )
                    logger.info(f"Placed buy order for SPY: Order ID {order.id}")
                    print(f"✅ Bought 1 share of SPY")
                except Exception as e:
                    logger.warning(f"Could not place order: {str(e)}")

            logger.info("Trading cycle completed")

        except Exception as e:
            logger.error(f"Error in trading cycle: {str(e)}")

def setup_scheduled_trading():
    """
    Set up automated trading schedule
    Runs every 30 minutes during market hours
    """
    trader = ExtendedAlpacaTrader()

    # Schedule the trading cycle every 30 minutes
    schedule.every(30).minutes.do(trader.run_trading_cycle)

    # Also run position check every hour
    schedule.every().hour.do(trader.check_all_positions)

    logger.info("Scheduled trading configured:")
    logger.info("- Trading cycle: Every 30 minutes")
    logger.info("- Position check: Every hour")

    print("\n🤖 Automated Trading Bot Started")
    print("📅 Schedule:")
    print("   - Trading cycle: Every 30 minutes")
    print("   - Position check: Every hour")
    print("\nPress Ctrl+C to stop\n")

    # Keep the scheduler running
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Check schedule every minute
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
            print("\n⏹️ Automated trading stopped")
            break
        except Exception as e:
            logger.error(f"Scheduler error: {str(e)}")
            time.sleep(60)

def main():
    """Main function with menu options"""
    trader = ExtendedAlpacaTrader()

    while True:
        print("\n" + "="*60)
        print(" ALPACA EXTENDED TRADING BOT ".center(60, "="))
        print("="*60)
        print("\n1. Check all positions and holdings")
        print("2. Run single trading cycle")
        print("3. Start automated trading (every 30 minutes)")
        print("4. View account information")
        print("5. Exit")
        print("\n" + "="*60)

        choice = input("\nSelect option (1-5): ").strip()

        if choice == '1':
            trader.check_all_positions()
        elif choice == '2':
            trader.run_trading_cycle()
        elif choice == '3':
            setup_scheduled_trading()
        elif choice == '4':
            account = trader.api.get_account()
            print(f"\n📊 Account Status: {account.status}")
            print(f"💰 Portfolio Value: ${float(account.portfolio_value):,.2f}")
            print(f"💵 Cash: ${float(account.cash):,.2f}")
            print(f"🛒 Buying Power: ${float(account.buying_power):,.2f}")
        elif choice == '5':
            print("\n👋 Goodbye!")
            logger.info("Application terminated by user")
            break
        else:
            print("\n❌ Invalid option, please try again")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        print(f"\n❌ Fatal error: {str(e)}")