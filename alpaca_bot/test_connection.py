#!/usr/bin/env python3
"""
Quick test script to verify Alpaca API connection
"""

import os
import sys
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient

# Fix Windows encoding issues
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

def test_connection():
    """Test the API connection"""
    try:
        # Get credentials
        api_key = os.getenv('APCA_API_KEY_ID')
        api_secret = os.getenv('APCA_API_SECRET_KEY')

        if not api_key or not api_secret:
            print("[ERROR] Missing API credentials in .env file")
            return False

        print(f"[INFO] API Key: {api_key[:10]}...")
        print(f"[INFO] Secret: {api_secret[:10]}...")

        # Create client
        print("\n[CONNECTING] Connecting to Alpaca Paper Trading API...")
        client = TradingClient(
            api_key=api_key,
            secret_key=api_secret,
            paper=True
        )

        # Test connection by getting account
        print("[FETCHING] Getting account information...")
        account = client.get_account()

        print("\n[SUCCESS] Connected to Alpaca API!")
        print(f"   Account Status: {account.status}")
        print(f"   Buying Power: ${float(account.buying_power):,.2f}")
        print(f"   Cash: ${float(account.cash):,.2f}")
        print(f"   Portfolio Value: ${float(account.equity):,.2f}")

        # Check market status
        clock = client.get_clock()
        market_status = "OPEN" if clock.is_open else "CLOSED"
        print(f"\n[MARKET] Status: {market_status}")
        print(f"   Next Open: {clock.next_open}")
        print(f"   Next Close: {clock.next_close}")

        return True

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        print("\nPossible issues:")
        print("1. Check your API credentials in .env file")
        print("2. Ensure you're using paper trading credentials")
        print("3. Check your internet connection")
        return False

if __name__ == "__main__":
    print("="*50)
    print(" ALPACA API CONNECTION TEST ".center(50))
    print("="*50)

    if test_connection():
        print("\n[SUCCESS] Your Alpaca bot is ready to trade!")
    else:
        print("\n[WARNING] Please fix the issues above before running the trading bot")