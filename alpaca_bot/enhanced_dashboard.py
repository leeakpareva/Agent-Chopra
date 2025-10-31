#!/usr/bin/env python3
"""
Enhanced Trading Dashboard with AI Assistant Integration
Combines the trading interface with intelligent AI analysis
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import os
from dotenv import load_dotenv
from streamlit_autorefresh import st_autorefresh

# Import our components
from trading_dashboard import TradingDashboard
from ai_trading_assistant import AITradingAssistant

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Enhanced Trading Dashboard with AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with AI theme
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }

    .ai-section {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }

    .insight-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
        margin: 1rem 0;
    }

    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }

    .metric-container:hover {
        transform: translateY(-2px);
    }

    .ai-response {
        background-color: #f8f9ff;
        border: 1px solid #e1e5fe;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        white-space: pre-wrap;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 8px 8px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'trading_dashboard' not in st.session_state:
        st.session_state.trading_dashboard = TradingDashboard()

    if 'ai_assistant' not in st.session_state:
        st.session_state.ai_assistant = None

    if 'last_ai_update' not in st.session_state:
        st.session_state.last_ai_update = None

def main():
    """Main enhanced dashboard function"""

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Enhanced Trading Dashboard</h1>
        <p>Professional Trading Interface with AI-Powered Analysis</p>
        <small>Paper Trading • Real-time Data • Intelligent Insights</small>
    </div>
    """, unsafe_allow_html=True)

    # Initialize components
    initialize_session_state()
    dashboard = st.session_state.trading_dashboard

    # Sidebar configuration
    st.sidebar.title("⚙️ Dashboard Controls")

    # AI Assistant Configuration
    st.sidebar.subheader("🤖 AI Assistant")
    openai_key = st.sidebar.text_input(
        "OpenAI API Key:",
        type="password",
        help="Enter your OpenAI API key to enable AI features"
    )

    if openai_key and not st.session_state.ai_assistant:
        try:
            st.session_state.ai_assistant = AITradingAssistant(openai_key)
            st.sidebar.success("✅ AI Assistant activated!")
        except Exception as e:
            st.sidebar.error(f"❌ AI initialization failed: {str(e)}")

    # Auto-refresh settings
    st.sidebar.subheader("🔄 Auto-refresh")
    refresh_rate = st.sidebar.selectbox(
        "Refresh interval (seconds)",
        [0, 10, 30, 60, 300],
        index=2
    )

    if refresh_rate > 0:
        st_autorefresh(interval=refresh_rate * 1000, key="datarefresh")

    # Update AI knowledge base
    if st.session_state.ai_assistant:
        if st.sidebar.button("🧠 Update AI Knowledge"):
            with st.sidebar:
                with st.spinner("Updating AI knowledge..."):
                    success = st.session_state.ai_assistant.update_knowledge_base()
                    if success:
                        st.success("Knowledge base updated!")
                        st.session_state.last_ai_update = datetime.now()
                    else:
                        st.error("Update failed")

        if st.session_state.last_ai_update:
            st.sidebar.caption(f"Last AI update: {st.session_state.last_ai_update.strftime('%H:%M:%S')}")

    # Main content tabs
    if st.session_state.ai_assistant:
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Trading Dashboard",
            "🤖 AI Chat",
            "📈 AI Insights",
            "🎯 Portfolio Analysis",
            "💡 Recommendations"
        ])
    else:
        tab1, tab_setup = st.tabs(["📊 Trading Dashboard", "🔧 Setup"])

        with tab_setup:
            st.markdown("""
            <div class="ai-section">
                <h3>🤖 Enable AI Assistant</h3>
                <p>Get intelligent trading insights powered by GPT-4!</p>
            </div>
            """, unsafe_allow_html=True)

            st.info("💡 **Enter your OpenAI API key in the sidebar to unlock AI features:**")
            st.markdown("""
            **AI Features Include:**
            - 📊 Automated trading performance analysis
            - 🎯 Portfolio optimization suggestions
            - 💰 Risk management insights
            - 🤖 Interactive chat about your trades
            - 📈 Market analysis and recommendations

            **How to get an OpenAI API key:**
            1. Visit https://platform.openai.com/
            2. Sign up or log in
            3. Go to API Keys section
            4. Create a new key
            5. Paste it in the sidebar
            """)

    # Trading Dashboard Tab
    with tab1:
        # Market Status
        market_data = dashboard.get_market_status()
        if market_data:
            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                market_status_class = "🟢" if market_data['is_open'] else "🔴"
                st.markdown(f"**Market Status:** {market_status_class} {'OPEN' if market_data['is_open'] else 'CLOSED'}")

            with col2:
                if market_data['is_open']:
                    st.write(f"Closes: {market_data['next_close'].strftime('%H:%M')}")
                else:
                    st.write(f"Opens: {market_data['next_open'].strftime('%m/%d %H:%M')}")

            with col3:
                st.caption(f"Updated: {datetime.now().strftime('%H:%M:%S')}")

        # Account Overview
        account_data = dashboard.get_account_data()
        if account_data:
            st.subheader("💼 Account Overview")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Portfolio Value", f"${account_data['equity']:,.2f}")

            with col2:
                st.metric("Buying Power", f"${account_data['buying_power']:,.2f}")

            with col3:
                st.metric("Cash Balance", f"${account_data['cash']:,.2f}")

            with col4:
                status_emoji = "🟢" if account_data['status'] == 'ACTIVE' else "🔴"
                st.metric("Status", f"{status_emoji} {account_data['status']}")

        # Positions
        st.subheader("📊 Current Positions")
        positions_df = dashboard.get_positions()

        if not positions_df.empty:
            # Enhanced positions display
            st.dataframe(
                positions_df.style.format({
                    'Avg Entry': '${:.2f}',
                    'Current Price': '${:.2f}',
                    'Market Value': '${:,.2f}',
                    'Unrealized P/L': '${:,.2f}',
                    'Unrealized P/L %': '{:.2f}%'
                }).applymap(
                    lambda x: 'color: green; font-weight: bold' if isinstance(x, (int, float)) and x > 0
                    else 'color: red; font-weight: bold' if isinstance(x, (int, float)) and x < 0
                    else '',
                    subset=['Unrealized P/L', 'Unrealized P/L %']
                ),
                use_container_width=True
            )

            # Chart
            pnl_chart = dashboard.create_pnl_chart(positions_df)
            if pnl_chart:
                st.plotly_chart(pnl_chart, use_container_width=True)

            # Portfolio metrics
            total_value = positions_df['Market Value'].sum()
            total_pnl = positions_df['Unrealized P/L'].sum()

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Position Value", f"${total_value:,.2f}")
            with col2:
                pnl_color = "normal" if total_pnl >= 0 else "inverse"
                st.metric("Total Unrealized P/L", f"${total_pnl:,.2f}", delta_color=pnl_color)
            with col3:
                st.metric("Open Positions", len(positions_df))
        else:
            st.info("📭 No open positions")

        # Quick Trading Panel
        with st.expander("🚀 Quick Trade", expanded=False):
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                symbol = st.text_input("Symbol", "AAPL", key="quick_symbol").upper()

            with col2:
                quantity = st.number_input("Quantity", min_value=1, value=1, key="quick_qty")

            with col3:
                side = st.selectbox("Side", ["BUY", "SELL"], key="quick_side")

            with col4:
                if st.button("Place Order", key="quick_trade"):
                    result = dashboard.place_order(symbol, quantity, side.lower())
                    if result['success']:
                        st.success(f"✅ Order placed! ID: {result['order_id']}")
                    else:
                        st.error(f"❌ Order failed: {result['error']}")

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

    # AI Features (only if assistant is available)
    if st.session_state.ai_assistant:
        ai_assistant = st.session_state.ai_assistant

        with tab2:  # AI Chat
            st.subheader("🤖 Chat with AI Trading Assistant")

            if 'chat_history' not in st.session_state:
                st.session_state.chat_history = []

            # Chat interface
            with st.container():
                # Display chat history
                for i, (question, answer) in enumerate(st.session_state.chat_history):
                    st.markdown(f"**You:** {question}")
                    st.markdown(f"<div class='ai-response'>🤖 **AI:** {answer}</div>", unsafe_allow_html=True)

                # Input for new question
                question = st.text_area("Ask me anything about your trading:", height=100)

                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button("Send", use_container_width=True):
                        if question.strip():
                            with st.spinner("AI is analyzing your data..."):
                                answer = ai_assistant.query(question)
                                st.session_state.chat_history.append((question, answer))
                                st.rerun()

                with col2:
                    if st.button("Clear Chat", use_container_width=True):
                        st.session_state.chat_history = []
                        st.rerun()

        with tab3:  # AI Insights
            st.subheader("📈 AI-Generated Trading Insights")

            if st.button("🧠 Generate Fresh Insights", use_container_width=True):
                with st.spinner("AI is analyzing your trading patterns..."):
                    insights = ai_assistant.get_trading_insights()

                st.markdown("""
                <div class="insight-card">
                <h4>🎯 AI Analysis Results</h4>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"<div class='ai-response'>{insights}</div>", unsafe_allow_html=True)

        with tab4:  # Portfolio Analysis
            st.subheader("🎯 AI Portfolio Analysis")

            if st.button("📊 Analyze My Portfolio", use_container_width=True):
                with st.spinner("AI is analyzing your portfolio composition..."):
                    analysis = ai_assistant.analyze_portfolio()

                st.markdown("""
                <div class="insight-card">
                <h4>📈 Portfolio Analysis</h4>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"<div class='ai-response'>{analysis}</div>", unsafe_allow_html=True)

        with tab5:  # Recommendations
            st.subheader("💡 AI Trading Recommendations")

            # Market context input
            market_context = st.text_area(
                "Current market context (optional):",
                placeholder="e.g., 'Markets are volatile due to Fed announcement', 'Tech earnings season approaching'",
                height=80
            )

            if st.button("🎯 Get AI Recommendations", use_container_width=True):
                with st.spinner("AI is generating personalized recommendations..."):
                    recommendations = ai_assistant.get_trade_recommendations(market_context)

                st.markdown("""
                <div class="insight-card">
                <h4>🚀 Personalized Trading Recommendations</h4>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"<div class='ai-response'>{recommendations}</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.caption(f"🕐 Last updated: {datetime.now().strftime('%H:%M:%S')}")

    with col2:
        st.caption("🔄 Auto-refresh enabled" if refresh_rate > 0 else "🔄 Manual refresh")

    with col3:
        st.caption("📈 Paper Trading Mode")

    with col4:
        if st.session_state.ai_assistant:
            st.caption("🤖 AI Assistant: Active")
        else:
            st.caption("🤖 AI Assistant: Inactive")

if __name__ == "__main__":
    main()