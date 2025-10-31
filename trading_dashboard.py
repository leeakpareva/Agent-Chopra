#!/usr/bin/env python3
"""
Professional Alpaca Trading Dashboard
Modern web-based UI for the trading bot using Streamlit
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
import os
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest, GetOrdersRequest
from alpaca.trading.enums import OrderSide, TimeInForce, QueryOrderStatus
from alpaca.common.exceptions import APIError
from streamlit_autorefresh import st_autorefresh

# Load environment variables
load_dotenv()

# Page configuration removed - handled by main dashboard

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79 0%, #2c5f8a 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #1f4e79;
        margin-bottom: 1rem;
    }

    .status-active {
        background-color: #d4edda;
        color: #155724;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }

    .status-inactive {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }

    .market-open {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }

    .market-closed {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }

    .order-success {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }

    .order-error {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }

    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }

    .stMetric {
        background-color: white;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

class TradingDashboard:
    """Main dashboard class for the Alpaca trading interface"""

    def __init__(self):
        """Initialize the dashboard"""
        if 'client' not in st.session_state:
            self._initialize_client()

        if 'last_refresh' not in st.session_state:
            st.session_state.last_refresh = datetime.now()

        if 'orders_history' not in st.session_state:
            st.session_state.orders_history = []

    def _initialize_client(self):
        """Initialize Alpaca client"""
        try:
            api_key = os.getenv('APCA_API_KEY_ID')
            api_secret = os.getenv('APCA_API_SECRET_KEY')

            if not api_key or not api_secret:
                st.error("❌ Missing API credentials. Please check your .env file.")
                st.stop()

            st.session_state.client = TradingClient(
                api_key=api_key,
                secret_key=api_secret,
                paper=True
            )

            # Test connection
            account = st.session_state.client.get_account()
            st.session_state.connected = True

        except Exception as e:
            st.error(f"❌ Failed to connect to Alpaca API: {str(e)}")
            st.session_state.connected = False
            st.stop()

    def get_account_data(self):
        """Get account information"""
        try:
            account = st.session_state.client.get_account()
            return {
                'status': account.status,
                'buying_power': float(account.buying_power),
                'cash': float(account.cash),
                'equity': float(account.equity),
                'day_trading_buying_power': float(account.daytrading_buying_power) if account.daytrading_buying_power else 0,
                'pattern_day_trader': account.pattern_day_trader,
                'account_blocked': account.account_blocked,
                'trading_blocked': account.trading_blocked
            }
        except Exception as e:
            st.error(f"Error fetching account data: {str(e)}")
            return None

    def get_positions(self):
        """Get current positions"""
        try:
            positions = st.session_state.client.get_all_positions()
            if not positions:
                return []

            position_data = []
            for pos in positions:
                position_data.append({
                    'Symbol': pos.symbol,
                    'Quantity': float(pos.qty),
                    'Avg Entry': float(pos.avg_entry_price),
                    'Current Price': float(pos.current_price) if pos.current_price else 0,
                    'Market Value': float(pos.market_value),
                    'Unrealized P/L': float(pos.unrealized_pl) if pos.unrealized_pl else 0,
                    'Unrealized P/L %': float(pos.unrealized_plpc) * 100 if pos.unrealized_plpc else 0,
                    'Side': pos.side
                })

            return pd.DataFrame(position_data)
        except Exception as e:
            st.error(f"Error fetching positions: {str(e)}")
            return pd.DataFrame()

    def get_orders(self, limit=20):
        """Get recent orders"""
        try:
            request = GetOrdersRequest(
                status=QueryOrderStatus.ALL,
                limit=limit,
                nested=False
            )
            orders = st.session_state.client.get_orders(filter=request)

            if not orders:
                return pd.DataFrame()

            order_data = []
            for order in orders:
                order_data.append({
                    'Time': order.submitted_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'Symbol': order.symbol,
                    'Side': str(order.side).upper(),
                    'Type': str(order.order_type).upper(),
                    'Quantity': order.qty,
                    'Status': str(order.status).upper(),
                    'Filled Qty': order.filled_qty if order.filled_qty else 0,
                    'Price': order.limit_price if order.limit_price else 'Market'
                })

            return pd.DataFrame(order_data)
        except Exception as e:
            st.error(f"Error fetching orders: {str(e)}")
            return pd.DataFrame()

    def get_market_status(self):
        """Get market status"""
        try:
            clock = st.session_state.client.get_clock()
            return {
                'is_open': clock.is_open,
                'next_open': clock.next_open,
                'next_close': clock.next_close,
                'timestamp': clock.timestamp
            }
        except Exception as e:
            st.error(f"Error fetching market status: {str(e)}")
            return None

    def place_order(self, symbol, qty, side, order_type='market', limit_price=None):
        """Place an order"""
        try:
            order_side = OrderSide.BUY if side.lower() == 'buy' else OrderSide.SELL

            if order_type.lower() == 'market':
                request = MarketOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side=order_side,
                    time_in_force=TimeInForce.DAY
                )
            else:  # Limit order
                request = LimitOrderRequest(
                    symbol=symbol,
                    qty=qty,
                    side=order_side,
                    time_in_force=TimeInForce.DAY,
                    limit_price=limit_price
                )

            order = st.session_state.client.submit_order(order_data=request)
            return {
                'success': True,
                'order_id': str(order.id),
                'symbol': order.symbol,
                'side': str(order.side),
                'qty': order.qty,
                'status': str(order.status)
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def create_pnl_chart(self, positions_df):
        """Create P&L visualization"""
        if positions_df.empty:
            return None

        # Create a pie chart for position distribution
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Position Distribution by Market Value', 'Unrealized P&L by Symbol'),
            specs=[[{'type': 'domain'}, {'type': 'bar'}]]
        )

        # Pie chart for position distribution
        fig.add_trace(
            go.Pie(
                labels=positions_df['Symbol'],
                values=positions_df['Market Value'].abs(),
                name="Market Value"
            ),
            row=1, col=1
        )

        # Bar chart for P&L
        colors = ['green' if x >= 0 else 'red' for x in positions_df['Unrealized P/L']]

        fig.add_trace(
            go.Bar(
                x=positions_df['Symbol'],
                y=positions_df['Unrealized P/L'],
                marker_color=colors,
                name="P&L"
            ),
            row=1, col=2
        )

        fig.update_layout(
            title_text="Portfolio Overview",
            height=400,
            showlegend=False
        )

        return fig

def main():
    """Main dashboard function"""

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📈 Alpaca Trading Dashboard</h1>
        <p>Professional Paper Trading Interface</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize dashboard
    dashboard = TradingDashboard()

    # Auto-refresh every 30 seconds
    refresh_rate = st.sidebar.selectbox(
        "Auto-refresh rate (seconds)",
        [0, 10, 30, 60, 300],
        index=2
    )

    if refresh_rate > 0:
        st_autorefresh(interval=refresh_rate * 1000, key="datarefresh")

    # Sidebar
    st.sidebar.title("⚙️ Trading Controls")

    # Market Status
    market_data = dashboard.get_market_status()
    if market_data:
        market_status_class = "market-open" if market_data['is_open'] else "market-closed"
        market_status_text = "OPEN" if market_data['is_open'] else "CLOSED"

        st.sidebar.markdown(f"""
        <div class="{market_status_class}">
            🕐 Market: {market_status_text}
        </div>
        """, unsafe_allow_html=True)

        if not market_data['is_open']:
            st.sidebar.write(f"Next open: {market_data['next_open'].strftime('%Y-%m-%d %H:%M')}")
        else:
            st.sidebar.write(f"Closes at: {market_data['next_close'].strftime('%H:%M')}")

    # Trading Form
    st.sidebar.subheader("📋 Place Order")

    with st.sidebar.form("trading_form"):
        symbol = st.text_input("Symbol", value="AAPL", help="e.g., AAPL, TSLA, SPY").upper()
        quantity = st.number_input("Quantity", min_value=1, value=1)
        side = st.selectbox("Side", ["BUY", "SELL"])
        order_type = st.selectbox("Order Type", ["MARKET", "LIMIT"])

        limit_price = None
        if order_type == "LIMIT":
            limit_price = st.number_input("Limit Price", min_value=0.01, value=100.00, step=0.01)

        submit_order = st.form_submit_button("🚀 Place Order", use_container_width=True)

        if submit_order:
            if symbol and quantity:
                result = dashboard.place_order(symbol, quantity, side.lower(), order_type.lower(), limit_price)

                if result['success']:
                    st.success(f"✅ Order placed successfully!\nID: {result['order_id']}")
                else:
                    st.error(f"❌ Order failed: {result['error']}")
            else:
                st.error("Please fill in all required fields")

    # Quick Actions
    st.sidebar.subheader("⚡ Quick Actions")
    col1, col2 = st.sidebar.columns(2)

    with col1:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()

    with col2:
        if st.button("📊 Update Charts", use_container_width=True):
            st.rerun()

    # Main Content
    account_data = dashboard.get_account_data()

    if account_data:
        # Account Overview
        st.subheader("💼 Account Overview")

        # Account metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            status_class = "status-active" if account_data['status'] == 'ACTIVE' else "status-inactive"
            st.markdown(f"""
            <div class="metric-container">
                <h4>Account Status</h4>
                <div class="{status_class}">{account_data['status']}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.metric(
                "Portfolio Value",
                f"${account_data['equity']:,.2f}",
                delta=None
            )

        with col3:
            st.metric(
                "Buying Power",
                f"${account_data['buying_power']:,.2f}",
                delta=None
            )

        with col4:
            st.metric(
                "Cash Balance",
                f"${account_data['cash']:,.2f}",
                delta=None
            )

        # Positions
        st.subheader("📊 Current Positions")
        positions_df = dashboard.get_positions()

        if not positions_df.empty:
            # Display positions table
            st.dataframe(
                positions_df.style.format({
                    'Avg Entry': '${:.2f}',
                    'Current Price': '${:.2f}',
                    'Market Value': '${:,.2f}',
                    'Unrealized P/L': '${:,.2f}',
                    'Unrealized P/L %': '{:.2f}%'
                }).applymap(
                    lambda x: 'color: green' if isinstance(x, (int, float)) and x > 0
                    else 'color: red' if isinstance(x, (int, float)) and x < 0
                    else '',
                    subset=['Unrealized P/L', 'Unrealized P/L %']
                ),
                use_container_width=True
            )

            # P&L Chart
            pnl_chart = dashboard.create_pnl_chart(positions_df)
            if pnl_chart:
                st.plotly_chart(pnl_chart, use_container_width=True)

            # Portfolio summary
            total_market_value = positions_df['Market Value'].sum()
            total_unrealized_pnl = positions_df['Unrealized P/L'].sum()

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Position Value", f"${total_market_value:,.2f}")
            with col2:
                st.metric(
                    "Total Unrealized P/L",
                    f"${total_unrealized_pnl:,.2f}",
                    delta=f"{(total_unrealized_pnl/total_market_value)*100:.2f}%" if total_market_value != 0 else "0%"
                )
            with col3:
                st.metric("Open Positions", len(positions_df))
        else:
            st.info("📭 No open positions")

        # Order History
        st.subheader("📋 Recent Orders")
        orders_df = dashboard.get_orders()

        if not orders_df.empty:
            st.dataframe(
                orders_df.style.applymap(
                    lambda x: 'background-color: #d4edda' if x == 'FILLED'
                    else 'background-color: #f8d7da' if x in ['REJECTED', 'CANCELED']
                    else 'background-color: #fff3cd' if x in ['NEW', 'PENDING_NEW']
                    else '',
                    subset=['Status']
                ),
                use_container_width=True
            )
        else:
            st.info("📭 No recent orders")

        # Footer
        st.markdown("---")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.caption(f"🕐 Last updated: {datetime.now().strftime('%H:%M:%S')}")

        with col2:
            st.caption("🔄 Data refreshes automatically")

        with col3:
            st.caption("📈 Paper Trading Mode")

if __name__ == "__main__":
    main()