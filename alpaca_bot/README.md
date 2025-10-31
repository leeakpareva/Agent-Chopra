# Alpaca Paper Trading Bot 📈

A Python-based paper trading bot for the Alpaca Markets API with comprehensive logging and automation features.

## 📁 Folder Structure

```
alpaca_bot/
├── trading_bot.py          # Main trading script
├── extended_bot.py         # Extended version with scheduling
├── .env                    # Your API credentials (DO NOT COMMIT)
├── .env.template           # Template for environment variables
├── .gitignore             # Git ignore file
├── requirements.txt        # Python dependencies
├── README.md              # Documentation
└── logs/                  # Log files directory
    ├── trading.log        # All trading activities
    └── errors.log         # Error logs only
```

## 🚀 Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Credentials
1. Copy `.env.template` to `.env`
2. Add your Alpaca API credentials to `.env`

### 3. Run the Trading Bot
```bash
# Basic trading bot
python trading_bot.py

# Extended bot with menu and scheduling
python extended_bot.py
```

## 📋 Requirements.txt Content

```
alpaca-trade-api==3.1.1
python-dotenv==1.0.0
pandas==2.0.3
numpy==1.24.3
schedule==1.2.0  # For extended_bot.py only
```

## 🔑 Sample .env Template

```env
# Alpaca Paper Trading API Credentials
APCA_API_KEY_ID=YOUR_API_KEY_HERE
APCA_API_SECRET_KEY=YOUR_SECRET_KEY_HERE
APCA_API_BASE_URL=https://paper-api.alpaca.markets
```

## 📊 Example Output (Successful Run)

```
============================================================
========== ALPACA PAPER TRADING BOT - STARTING ===========
============================================================

📌 Step 1: Checking market status...
🕐 Market Status: OPEN
   Current Time: 2024-01-15 14:30:00-05:00
   Next Open: 2024-01-16 09:30:00-05:00
   Next Close: 2024-01-15 16:00:00-05:00

📌 Step 2: Getting account information...

==================================================
ACCOUNT INFORMATION
==================================================
Account Status: ACTIVE
Buying Power: $100,000.00
Cash Balance: $100,000.00
Portfolio Value: $100,000.00
Pattern Day Trader: False
==================================================

📌 Step 3: Checking current positions...
📊 No open positions

📌 Step 4: Placing BUY order for AAPL...

✅ Market Order Placed:
   Symbol: AAPL
   Side: BUY
   Quantity: 1
   Order ID: 7a5c61f2-1234-5678-90ab-cdef12345678
   Status: new

⏳ Waiting 60 seconds before selling...
   60 seconds remaining...
   50 seconds remaining...
   40 seconds remaining...
   30 seconds remaining...
   20 seconds remaining...
   10 seconds remaining...

📌 Step 6: Placing SELL order for AAPL...

✅ Market Order Placed:
   Symbol: AAPL
   Side: SELL
   Quantity: 1
   Order ID: 8b6d72g3-2345-6789-01bc-defg23456789
   Status: new

📌 Step 7: Getting recent order history...

==================================================
LAST 5 ORDERS
==================================================

Symbol: AAPL
  Side: SELL
  Quantity: 1
  Status: filled
  Type: market
  Submitted: 2024-01-15T14:31:00Z
  Filled: 2024-01-15T14:31:01Z

Symbol: AAPL
  Side: BUY
  Quantity: 1
  Status: filled
  Type: market
  Submitted: 2024-01-15T14:30:00Z
  Filled: 2024-01-15T14:30:01Z
==================================================

📌 Step 8: Final position check...
📊 No open positions

📌 Step 9: Final account status...

==================================================
ACCOUNT INFORMATION
==================================================
Account Status: ACTIVE
Buying Power: $99,998.50
Cash Balance: $99,998.50
Portfolio Value: $99,998.50
Pattern Day Trader: False
==================================================

============================================================
========== TRADING BOT EXECUTION COMPLETED ===========
============================================================
```

## 🔧 Features

### Main Trading Bot (`trading_bot.py`)
- ✅ Secure API connection using environment variables
- ✅ Account status and balance checking
- ✅ Market order placement (buy/sell)
- ✅ Order history retrieval
- ✅ Position monitoring
- ✅ Market status checking
- ✅ Comprehensive error handling
- ✅ Detailed logging to file

### Extended Trading Bot (`extended_bot.py`)
All features above plus:
- 📊 Detailed position analysis with P/L
- ⏰ Automated trading every 30 minutes
- 📈 Portfolio weight calculations
- 🎛️ Interactive menu system
- 📝 Enhanced logging with multiple handlers

## ⚠️ Important Notes

1. **Paper Trading Only**: This bot uses Alpaca's paper trading API. No real money is involved.

2. **API Credentials Security**:
   - Never commit your `.env` file to version control
   - Keep your API keys secure
   - Use the `.env.template` as reference

3. **Market Hours**: The bot checks if the market is open before trading. Orders placed outside market hours will be queued or rejected.

4. **Rate Limits**: Be aware of Alpaca's API rate limits. The bot includes appropriate delays.

## 🐛 Troubleshooting

1. **Import Error**: Make sure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. **API Authentication Error**: Verify your credentials in `.env` file

3. **Market Closed**: The bot will show market status. Trading is only possible during market hours.

4. **Insufficient Buying Power**: Check your paper account balance on Alpaca's website

## 📝 Logging

- All activities are logged to `logs/trading.log`
- Errors are additionally logged to `logs/errors.log`
- Console output shows real-time trading activities

## 🚦 Running the Bot

### Quick Test Run
```bash
python trading_bot.py
```

### Automated Trading (Every 30 minutes)
```bash
python extended_bot.py
# Select option 3 from the menu
```

### Check Positions Only
```bash
python extended_bot.py
# Select option 1 from the menu
```

## 📚 Additional Resources

- [Alpaca Markets Documentation](https://docs.alpaca.markets/)
- [Alpaca Python SDK](https://github.com/alpacahq/alpaca-trade-api-python)
- [Paper Trading Guide](https://alpaca.markets/docs/trading/paper-trading/)

---

**Disclaimer**: This is for educational and paper trading purposes only. Always test thoroughly before considering any live trading implementation.