# Alpaca Trading Bot - Setup Guide

## ⚠️ API Credential Issue Detected

The provided API credentials are returning "unauthorized" error. Here's how to fix it:

## Step 1: Get Valid Paper Trading Credentials

1. **Go to Alpaca Markets**: https://app.alpaca.markets/
2. **Sign up or Log in** to your account
3. **Select Paper Trading** (Important: NOT live trading)
4. **Navigate to API Keys** section
5. **Generate New API Key** if needed
6. **Copy both**:
   - API Key ID
   - Secret Key (shown only once!)

## Step 2: Update Your Credentials

Edit the `.env` file with your new credentials:

```env
APCA_API_KEY_ID=YOUR_NEW_KEY_HERE
APCA_API_SECRET_KEY=YOUR_NEW_SECRET_HERE
APCA_API_BASE_URL=https://paper-api.alpaca.markets
```

## Step 3: Verify Your Setup

Run the test script:
```bash
python test_connection.py
```

You should see:
```
[SUCCESS] Connected to Alpaca API!
   Account Status: ACTIVE
   Buying Power: $100,000.00
   ...
```

## Common Issues & Solutions

### 1. "Unauthorized" Error
- **Cause**: Invalid or expired credentials
- **Solution**: Generate new API keys from Alpaca dashboard

### 2. Wrong Environment
- **Cause**: Using live trading keys for paper trading
- **Solution**: Make sure you're in Paper Trading mode on Alpaca dashboard

### 3. API Key Format
- **Cause**: Extra spaces or incorrect format
- **Solution**: Copy keys exactly without spaces

### 4. Account Not Activated
- **Cause**: Paper account needs activation
- **Solution**: Click "Reset Paper Account" in Alpaca dashboard

## Quick Checklist

- [ ] Logged into Alpaca Markets
- [ ] Selected "Paper Trading" mode
- [ ] Generated paper trading API keys
- [ ] Updated .env file with new keys
- [ ] No extra spaces in credentials
- [ ] Ran test_connection.py successfully

## Need More Help?

1. **Alpaca Documentation**: https://docs.alpaca.markets/
2. **Paper Trading Setup**: https://alpaca.markets/docs/trading/paper-trading/
3. **API Authentication**: https://docs.alpaca.markets/docs/api-documentation/api-v2/authentication/

## Installation Summary

### Working Installation:
```bash
# Already installed successfully:
✅ alpaca-py (0.43.1)
✅ python-dotenv (1.0.0)
✅ pandas (2.0.3)
✅ requests (2.31.0)
```

### To Run the Bot:
1. Fix API credentials (follow steps above)
2. Test connection: `python test_connection.py`
3. Run simple bot: `python trading_bot_v2.py`

## Files Created:

- `trading_bot_v2.py` - Main trading bot (Windows compatible)
- `test_connection.py` - Connection tester
- `.env` - Your credentials (needs valid keys)
- `.env.template` - Template for others
- `requirements_simple.txt` - Working dependencies

---

**Remember**: This is PAPER TRADING only - no real money involved!