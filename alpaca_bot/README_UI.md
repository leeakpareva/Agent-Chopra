# Alpaca Trading Dashboard UI 📊

## 🎯 Professional Modern Trading Interface

A sleek, professional web-based dashboard for your Alpaca paper trading bot with real-time updates and comprehensive trading features.

## ✨ Features

### 📈 **Account Overview**
- Real-time account status and metrics
- Portfolio value, buying power, and cash balance
- Visual status indicators

### 📊 **Position Management**
- Live positions with P&L tracking
- Interactive charts and visualizations
- Position distribution pie charts
- Unrealized P&L bar charts

### 🚀 **Trading Interface**
- Quick order placement (Market & Limit orders)
- Symbol search and validation
- Real-time order status updates

### 📋 **Order History**
- Complete order history with status tracking
- Color-coded status indicators
- Filterable and sortable data

### ⚡ **Real-time Updates**
- Auto-refresh every 10/30/60 seconds
- Live market status indicator
- Instant data synchronization

## 🚀 Quick Start

### 1. Launch the Dashboard
```bash
# Simple launch
python launch_dashboard.py

# Or directly with Streamlit
streamlit run trading_dashboard.py
```

### 2. Access the Interface
- Dashboard will open automatically in your browser
- Default URL: http://localhost:8501
- Mobile responsive design

## 🎨 Modern UI Features

### **Professional Design**
- Clean, modern interface
- Gradient headers and professional color scheme
- Responsive layout for all screen sizes

### **Interactive Elements**
- Real-time charts and graphs
- Hover effects and animations
- Intuitive navigation

### **Visual Indicators**
- 🟢 Green for profits and active status
- 🔴 Red for losses and inactive status
- 🟡 Yellow for pending states
- 📊 Clear data visualization

## 📱 Interface Sections

### **Sidebar Controls**
- 🕐 Market status indicator
- 📋 Order placement form
- ⚡ Quick action buttons
- 🔄 Auto-refresh settings

### **Main Dashboard**
- 💼 Account overview metrics
- 📊 Current positions table
- 📈 P&L visualization charts
- 📋 Recent orders history

## 🔧 Configuration Options

### **Auto-Refresh Rates**
- Off (manual refresh only)
- 10 seconds (high frequency)
- 30 seconds (recommended)
- 60 seconds (standard)
- 300 seconds (low frequency)

### **Order Types Supported**
- Market Orders (immediate execution)
- Limit Orders (price-specific)
- Buy and Sell operations

## 📊 Dashboard Screenshots

### Main Dashboard
```
╔══════════════════════════════════════════════════════════╗
║                📈 Alpaca Trading Dashboard               ║
║                Professional Paper Trading Interface      ║
╚══════════════════════════════════════════════════════════╝

💼 Account Overview
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ Status      │ Portfolio   │ Buying Power│ Cash Balance│
│ 🟢 ACTIVE   │ $100,000.00 │ $50,000.00  │ $25,000.00  │
└─────────────┴─────────────┴─────────────┴─────────────┘

📊 Current Positions
┌────────┬─────┬───────┬──────────┬────────────┬─────────┐
│ Symbol │ Qty │ Entry │ Current  │ Market Val │ P&L     │
├────────┼─────┼───────┼──────────┼────────────┼─────────┤
│ AAPL   │ 10  │ $150  │ $155.50  │ $1,555.00  │ +$55.00 │
│ TSLA   │ 5   │ $200  │ $195.00  │ $975.00    │ -$25.00 │
└────────┴─────┴───────┴──────────┴────────────┴─────────┘
```

## 🛠️ Technical Details

### **Built With**
- **Streamlit** - Modern web framework
- **Plotly** - Interactive visualizations
- **Pandas** - Data manipulation
- **Alpaca-py** - Trading API integration

### **Performance**
- Lightweight and fast
- Efficient data caching
- Optimized refresh cycles
- Minimal resource usage

## 🚀 Advanced Features

### **Real-time Charts**
- Portfolio distribution pie charts
- P&L bar charts with color coding
- Interactive hover information

### **Smart Refreshing**
- Configurable auto-refresh rates
- Manual refresh buttons
- Efficient data loading

### **Professional Styling**
- Modern CSS with gradients
- Responsive design
- Professional color scheme
- Clean typography

## 🔒 Security

- Paper trading only (no real money)
- Secure credential handling
- Local-only data processing
- No sensitive data logging

---

**Ready to trade with style!** 🎯

Launch your dashboard: `python launch_dashboard.py`