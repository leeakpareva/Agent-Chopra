#!/usr/bin/env python3
"""
Agent Chopra - Advanced AI Trading Platform
Complete trading dashboard with risk profiling, AI insights, and dark theme
"""

import streamlit as st

# Page configuration with dark theme - MUST BE FIRST
st.set_page_config(
    page_title="Agent Chopra - AI Trading Platform",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import os
import json
from dotenv import load_dotenv
from streamlit_autorefresh import st_autorefresh
import streamlit_authenticator as stauth

# Load environment variables first
load_dotenv()

# Import our enhanced components
from trading_dashboard import TradingDashboard
from ai_trading_assistant import AITradingAssistant
from risk_profiler import RiskProfiler, RiskProfile
from database.models import db_manager, User, RiskLevel

# Import new advanced features
try:
    from alpha_vantage_integration import (
        AlphaVantageAPI, MarketIntelligence,
        create_daily_pnl_dashboard, create_stock_watchlist, create_market_news_section
    )
    from brave_search_integration import (
        BraveSearchAPI, MarketResearcher,
        create_market_research_dashboard, create_quick_search_widget
    )
    from voice_integration import (
        VoiceAssistant, create_voice_interface, create_voice_quick_actions
    )
    ADVANCED_FEATURES_AVAILABLE = True
except ImportError as e:
    st.warning(f"Some advanced features unavailable: {e}")
    ADVANCED_FEATURES_AVAILABLE = False

# LangSmith integration (set via environment variables)
# Environment variables should be set in .env file:
# LANGSMITH_TRACING=true
# LANGSMITH_ENDPOINT=https://api.smith.langchain.com
# LANGSMITH_API_KEY=your_langsmith_key_here
# LANGSMITH_PROJECT=your_project_name

# Agent Chopra Dark/Red Theme CSS
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');

    /* Global Variables */
    :root {
        --primary-red: #DC143C;
        --dark-red: #8B0000;
        --bright-red: #FF1744;
        --dark-bg: #0D1117;
        --darker-bg: #010409;
        --card-bg: #161B22;
        --border-color: #30363D;
        --text-primary: #F0F6FC;
        --text-secondary: #7D8590;
        --accent-gold: #FFD700;
        --success-green: #238636;
        --warning-orange: #FB8500;
    }

    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #0D1117 0%, #010409 50%, #0D1117 100%);
        color: var(--text-primary);
        font-family: 'Rajdhani', sans-serif;
    }

    /* Main Header */
    .main-header {
        background: linear-gradient(135deg, var(--primary-red) 0%, var(--dark-red) 50%, #000000 100%);
        color: var(--text-primary);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 0 30px rgba(220, 20, 60, 0.3);
        border: 1px solid var(--primary-red);
        font-family: 'Orbitron', monospace;
    }

    .main-header h1 {
        font-size: 3rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 10px rgba(220, 20, 60, 0.8);
        letter-spacing: 2px;
    }

    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }

    .main-header small {
        font-size: 0.9rem;
        opacity: 0.7;
    }

    /* Cards and Containers */
    .metric-container {
        background: linear-gradient(135deg, var(--card-bg) 0%, var(--darker-bg) 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        border: 1px solid var(--border-color);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .metric-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary-red), var(--bright-red), var(--primary-red));
    }

    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(220, 20, 60, 0.2);
        border-color: var(--primary-red);
    }

    /* AI Section Styling */
    .ai-section {
        background: linear-gradient(135deg, var(--primary-red) 0%, var(--dark-red) 100%);
        color: var(--text-primary);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 0 20px rgba(220, 20, 60, 0.4);
        border: 1px solid var(--bright-red);
    }

    .ai-section h3 {
        font-family: 'Orbitron', monospace;
        margin-bottom: 1rem;
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
    }

    /* Risk Profile Cards */
    .risk-card {
        background: linear-gradient(135deg, var(--card-bg) 0%, var(--darker-bg) 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
    }

    .risk-card:hover {
        border-color: var(--primary-red);
        box-shadow: 0 0 15px rgba(220, 20, 60, 0.3);
    }

    .risk-score {
        font-size: 2.5rem;
        font-weight: bold;
        color: var(--primary-red);
        text-align: center;
        font-family: 'Orbitron', monospace;
    }

    /* AI Response Styling */
    .ai-response {
        background: linear-gradient(135deg, var(--card-bg) 0%, var(--darker-bg) 100%);
        border: 1px solid var(--primary-red);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        white-space: pre-wrap;
        font-family: 'Rajdhani', sans-serif;
        box-shadow: 0 0 15px rgba(220, 20, 60, 0.2);
    }

    /* Status Indicators */
    .status-active {
        background: linear-gradient(135deg, var(--success-green), #2DA44E);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
    }

    .status-inactive {
        background: linear-gradient(135deg, var(--primary-red), var(--dark-red));
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
    }

    .market-open {
        background: linear-gradient(135deg, var(--success-green), #2DA44E);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: bold;
        display: inline-block;
        animation: pulse 2s infinite;
    }

    .market-closed {
        background: linear-gradient(135deg, var(--primary-red), var(--dark-red));
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: bold;
        display: inline-block;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(35, 134, 54, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(35, 134, 54, 0); }
        100% { box-shadow: 0 0 0 0 rgba(35, 134, 54, 0); }
    }

    /* Enhanced Sidebar Styling */
    .css-1d391kg, .css-1cypcdb, .stSidebar, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--card-bg) 0%, var(--darker-bg) 100%) !important;
        border-right: 2px solid var(--primary-red) !important;
    }

    .stSidebar .stSelectbox > div > div {
        background: var(--card-bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
    }

    .stSidebar .stTextInput > div > div > input {
        background: var(--card-bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
    }

    .stSidebar .stTextInput > div > div > input:focus {
        border-color: var(--primary-red) !important;
        box-shadow: 0 0 0 2px rgba(220, 20, 60, 0.2) !important;
    }

    .stSidebar .stButton > button {
        background: linear-gradient(135deg, var(--primary-red), var(--dark-red)) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }

    .stSidebar .stButton > button:hover {
        background: linear-gradient(135deg, var(--bright-red), var(--primary-red)) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(220, 20, 60, 0.4) !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: var(--darker-bg);
        border-radius: 10px;
        padding: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background: var(--card-bg);
        border-radius: 8px;
        border: 1px solid var(--border-color);
        color: var(--text-secondary);
        font-weight: 500;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: var(--primary-red);
        color: white;
        border-color: var(--bright-red);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary-red), var(--dark-red));
        color: white;
        border-color: var(--bright-red);
        box-shadow: 0 0 10px rgba(220, 20, 60, 0.5);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-red), var(--dark-red));
        color: white;
        border: 1px solid var(--bright-red);
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(220, 20, 60, 0.3);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, var(--bright-red), var(--primary-red));
        box-shadow: 0 4px 15px rgba(220, 20, 60, 0.5);
        transform: translateY(-1px);
    }

    /* Metrics */
    .stMetric {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 1rem;
        transition: all 0.3s ease;
    }

    .stMetric:hover {
        border-color: var(--primary-red);
        box-shadow: 0 0 10px rgba(220, 20, 60, 0.3);
    }

    /* Success/Error Messages */
    .stSuccess {
        background: linear-gradient(135deg, var(--success-green), #2DA44E);
        border-radius: 8px;
    }

    .stError {
        background: linear-gradient(135deg, var(--primary-red), var(--dark-red));
        border-radius: 8px;
    }

    /* Enhanced Data Tables and Position Intelligence */
    .stDataFrame {
        background: var(--card-bg) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid var(--border-color) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }

    .stDataFrame div[data-testid="stDataFrame"] > div {
        background: var(--card-bg) !important;
        color: var(--text-primary) !important;
    }

    .stDataFrame table {
        background: var(--card-bg) !important;
        color: var(--text-primary) !important;
    }

    .stDataFrame th {
        background: var(--darker-bg) !important;
        color: var(--text-primary) !important;
        border-bottom: 2px solid var(--primary-red) !important;
        font-weight: 600 !important;
    }

    .stDataFrame td {
        background: var(--card-bg) !important;
        color: var(--text-primary) !important;
        border-bottom: 1px solid var(--border-color) !important;
    }

    .stDataFrame tr:hover td {
        background: rgba(220, 20, 60, 0.1) !important;
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--darker-bg);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--primary-red);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--bright-red);
    }

    /* Loading Animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid var(--border-color);
        border-radius: 50%;
        border-top-color: var(--primary-red);
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    /* Agent Chopra Logo */
    .agent-logo {
        font-family: 'Orbitron', monospace;
        font-size: 2rem;
        font-weight: 900;
        background: linear-gradient(45deg, var(--primary-red), var(--accent-gold), var(--bright-red));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 0 0 20px rgba(220, 20, 60, 0.5);
    }

    /* Enhanced Button Styling */
    .stButton > button {
        padding: 12px 24px !important;
        margin: 8px 4px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        min-height: 48px !important;
        width: auto !important;
        text-align: center !important;
        border: 2px solid transparent !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #DC143C 0%, #B91C3C 100%) !important;
        color: white !important;
        border: 2px solid #DC143C !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #B91C3C 0%, #991B1B 100%) !important;
        border: 2px solid #B91C3C !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(220, 20, 60, 0.3) !important;
    }

    .stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #374151 0%, #1F2937 100%) !important;
        color: #F9FAFB !important;
        border: 2px solid #4B5563 !important;
    }

    .stButton > button[kind="secondary"]:hover {
        background: linear-gradient(135deg, #4B5563 0%, #374151 100%) !important;
        border: 2px solid #6B7280 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(75, 85, 99, 0.3) !important;
    }

    /* Tab styling improvements */
    .stTabs > div > div > div > div {
        padding: 12px 20px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }

    /* Selectbox styling */
    .stSelectbox > div > div {
        padding: 8px 12px !important;
        border-radius: 6px !important;
    }

    /* Text input styling */
    .stTextInput > div > div > input {
        padding: 12px 16px !important;
        border-radius: 6px !important;
        font-size: 16px !important;
    }

    /* Number input styling */
    .stNumberInput > div > div > input {
        padding: 12px 16px !important;
        border-radius: 6px !important;
        font-size: 16px !important;
    }
</style>
""", unsafe_allow_html=True)

class AgentChopra:
    """Main Agent Chopra application class"""

    def __init__(self):
        self.initialize_session_state()
        self.setup_database()

    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'trading_dashboard' not in st.session_state:
            st.session_state.trading_dashboard = TradingDashboard()

        if 'ai_assistant' not in st.session_state:
            st.session_state.ai_assistant = None

        if 'risk_profiler' not in st.session_state:
            st.session_state.risk_profiler = RiskProfiler()

        if 'user_risk_profile' not in st.session_state:
            st.session_state.user_risk_profile = None

        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        if 'authentication_status' not in st.session_state:
            st.session_state.authentication_status = None

        if 'last_ai_update' not in st.session_state:
            st.session_state.last_ai_update = None

        # Initialize new advanced features
        if ADVANCED_FEATURES_AVAILABLE:
            if 'alpha_vantage_api' not in st.session_state:
                st.session_state.alpha_vantage_api = AlphaVantageAPI()

            if 'market_intelligence' not in st.session_state:
                st.session_state.market_intelligence = MarketIntelligence(st.session_state.alpha_vantage_api)

            if 'brave_search_api' not in st.session_state:
                st.session_state.brave_search_api = BraveSearchAPI()

            if 'market_researcher' not in st.session_state:
                st.session_state.market_researcher = MarketResearcher(st.session_state.brave_search_api)

            if 'voice_assistant' not in st.session_state:
                st.session_state.voice_assistant = VoiceAssistant()

    def setup_database(self):
        """Setup database tables"""
        try:
            db_manager.create_tables()
        except Exception as e:
            st.error(f"Database setup error: {e}")

    def render_header(self):
        """Render the main header"""
        st.markdown("""
        <div class="main-header">
            <h1>🔥 AGENT CHOPRA</h1>
            <p>Advanced AI Trading Intelligence Platform</p>
            <small>Paper Trading • Real-time Analysis • Risk-Optimized • AI-Powered</small>
        </div>
        """, unsafe_allow_html=True)

    def render_sidebar(self):
        """Render sidebar controls"""
        st.sidebar.markdown('<div class="agent-logo">🔥 AGENT CHOPRA</div>', unsafe_allow_html=True)

        # AI Assistant Configuration
        st.sidebar.subheader("🤖 AI Intelligence")
        openai_key = st.sidebar.text_input(
            "OpenAI API Key:",
            type="password",
            help="Enter your OpenAI API key to unlock AI features"
        )

        if openai_key and not st.session_state.ai_assistant:
            try:
                with st.sidebar:
                    with st.spinner("Initializing AI..."):
                        st.session_state.ai_assistant = AITradingAssistant(openai_key)
                        st.success("✅ AI Assistant activated!")
            except Exception as e:
                st.sidebar.error(f"❌ AI initialization failed: {str(e)}")

        # Risk Profile Section
        st.sidebar.subheader("⚡ Risk Profile")
        if st.sidebar.button("Assess Risk Profile"):
            self.show_risk_assessment()

        if st.session_state.user_risk_profile:
            profile = st.session_state.user_risk_profile
            level_name = str(profile.level.name).replace('_', ' ').title() if hasattr(profile.level, 'name') else f"Level {profile.score}"
            full_name = f"{profile.first_name} {profile.last_name}".strip()

            st.sidebar.markdown(f"""
            <div class="risk-card">
                <div style="text-align: center; margin-bottom: 0.5rem;">
                    <strong style="color: #DC143C;">{full_name}</strong>
                </div>
                <div class="risk-score">{profile.score}/10</div>
                <div style="text-align: center; margin-top: 0.5rem;">
                    <strong>{level_name}</strong>
                </div>
                <div style="text-align: center; margin-top: 0.3rem; font-size: 0.8rem;">
                    <span style="color: #888;">Strategy: {profile.trading_strategy}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Auto-refresh settings
        st.sidebar.subheader("🔄 Auto-refresh")
        refresh_rate = st.sidebar.selectbox(
            "Refresh interval (seconds)",
            [0, 10, 30, 60, 300],
            index=2
        )

        if refresh_rate > 0:
            st_autorefresh(interval=refresh_rate * 1000, key="datarefresh")

        # AI Knowledge Update
        if st.session_state.ai_assistant:
            if st.sidebar.button("🧠 Update AI Knowledge"):
                with st.sidebar:
                    with st.spinner("Updating AI knowledge..."):
                        success = st.session_state.ai_assistant.update_knowledge_base()
                        if success:
                            st.success("Knowledge updated!")
                            st.session_state.last_ai_update = datetime.now()
                        else:
                            st.error("Update failed")

        return refresh_rate

    def show_risk_assessment(self):
        """Show enhanced 5-question risk assessment"""
        st.subheader("🎯 Personal Risk Profile Assessment")

        st.markdown("""
        <div style='background: linear-gradient(135deg, #1a1a1a 0%, #2d1b1b 100%);
                    padding: 20px; border-radius: 10px; margin-bottom: 20px;
                    border: 1px solid #DC143C;'>
            <p style='color: #888; margin: 0; text-align: center;'>
                Answer 3 essential questions to determine your personalized risk score (1-10)
            </p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("enhanced_risk_assessment"):
            # Personal Information
            st.markdown("### 👤 Personal Information")
            col1, col2 = st.columns(2)

            with col1:
                first_name = st.text_input("First Name", placeholder="Enter your first name")
            with col2:
                last_name = st.text_input("Last Name", placeholder="Enter your last name")

            st.markdown("### 📊 Risk Assessment Questions")

            # Get questions from risk profiler
            questions = st.session_state.risk_profiler.get_risk_questions()

            # Store answers
            answers = {}

            for i, q in enumerate(questions, 1):
                st.markdown(f"**Question {i}: {q['question']}**")
                st.caption(q['description'])

                # Create slider with custom labels
                value = st.slider(
                    f"Score (1-10)",
                    min_value=1,
                    max_value=10,
                    value=5,
                    key=q['id'],
                    help=f"{q['scale_low']} ← → {q['scale_high']}"
                )
                answers[q['id']] = value

                # Show scale info
                col1, col2 = st.columns(2)
                with col1:
                    st.caption(f"1️⃣ {q['scale_low']}")
                with col2:
                    st.caption(f"🔟 {q['scale_high']}")

                st.markdown("---")

            # Trading Strategy Selection
            st.markdown("### ⚙️ Trading Strategy (Optional)")
            strategies = st.session_state.risk_profiler.get_trading_strategies()
            strategy_names = [s['name'] for s in strategies]
            selected_strategy = st.selectbox(
                "Preferred Trading Strategy",
                strategy_names,
                help="Choose your preferred automated trading approach"
            )

            # Get selected strategy details
            strategy_details = next(s for s in strategies if s['name'] == selected_strategy)
            st.info(f"**{selected_strategy}**: {strategy_details['description']}")

            # Automated Trading Options
            automated_trading = st.checkbox("Enable Automated Trading", value=False)

            if automated_trading:
                col1, col2 = st.columns(2)
                with col1:
                    max_daily_trades = st.number_input("Max Daily Trades", min_value=1, max_value=20, value=3)
                with col2:
                    stop_loss_pct = st.number_input("Stop Loss %", min_value=1.0, max_value=20.0, value=5.0, step=0.5)

            submitted = st.form_submit_button("Calculate My Risk Profile", use_container_width=True)

            if submitted:
                if not first_name or not last_name:
                    st.error("Please enter your first and last name")
                    return

                # Prepare user data
                user_data = {
                    'first_name': first_name.strip(),
                    'last_name': last_name.strip(),
                    'trading_strategy': selected_strategy,
                    'automated_trading': automated_trading,
                    **answers
                }

                if automated_trading:
                    user_data['max_daily_trades'] = max_daily_trades
                    user_data['stop_loss_percentage'] = stop_loss_pct

                # Calculate risk profile with loading spinner
                with st.spinner("🔍 Calculating your personalized risk profile..."):
                    try:
                        risk_score, risk_profile = st.session_state.risk_profiler.assess_risk_profile(user_data)
                        st.session_state.user_risk_profile = risk_profile

                        # Risk profile calculated successfully

                        # Show results
                        st.success(f"✅ Risk Profile Created for {first_name} {last_name}")

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Risk Score", f"{risk_score}/10")
                        with col2:
                            level_name = str(risk_profile.level.name).replace('_', ' ').title() if hasattr(risk_profile.level, 'name') else f"Level {risk_score}"
                            st.metric("Risk Level", level_name)
                        with col3:
                            st.metric("Strategy", selected_strategy)

                    except Exception as e:
                        st.error(f"❌ Error calculating risk profile: {str(e)}")
                        return

                st.rerun()

    def render_trading_dashboard(self):
        """Render main trading dashboard"""
        dashboard = st.session_state.trading_dashboard

        # Market Status
        market_data = dashboard.get_market_status()
        if market_data:
            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                status_class = "market-open" if market_data['is_open'] else "market-closed"
                status_text = "🟢 MARKET OPEN" if market_data['is_open'] else "🔴 MARKET CLOSED"
                st.markdown(f'<div class="{status_class}">{status_text}</div>', unsafe_allow_html=True)

            with col2:
                if market_data['is_open']:
                    st.write(f"⏰ Closes: {market_data['next_close'].strftime('%H:%M')}")
                else:
                    st.write(f"⏰ Opens: {market_data['next_open'].strftime('%m/%d %H:%M')}")

            with col3:
                st.caption(f"🕐 {datetime.now().strftime('%H:%M:%S')}")

        # Account Overview
        account_data = dashboard.get_account_data()
        if account_data:
            st.subheader("💼 Portfolio Command Center")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown("""
                <div class="metric-container">
                    <h4>Portfolio Value</h4>
                    <div style="font-size: 1.5rem; color: #FFD700; font-weight: bold;">
                        ${:,.2f}
                    </div>
                </div>
                """.format(account_data['equity']), unsafe_allow_html=True)

            with col2:
                st.markdown("""
                <div class="metric-container">
                    <h4>Buying Power</h4>
                    <div style="font-size: 1.5rem; color: #00FF41; font-weight: bold;">
                        ${:,.2f}
                    </div>
                </div>
                """.format(account_data['buying_power']), unsafe_allow_html=True)

            with col3:
                st.markdown("""
                <div class="metric-container">
                    <h4>Cash Balance</h4>
                    <div style="font-size: 1.5rem; color: #00BFFF; font-weight: bold;">
                        ${:,.2f}
                    </div>
                </div>
                """.format(account_data['cash']), unsafe_allow_html=True)

            with col4:
                status_emoji = "🟢" if account_data['status'] == 'ACTIVE' else "🔴"
                status_class = "status-active" if account_data['status'] == 'ACTIVE' else "status-inactive"
                st.markdown(f"""
                <div class="metric-container">
                    <h4>Account Status</h4>
                    <div class="{status_class}">
                        {status_emoji} {account_data['status']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # User Risk Profile Dashboard
        if st.session_state.user_risk_profile:
            st.markdown("### 🎯 Personal Risk Profile")

            risk_profile = st.session_state.user_risk_profile
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(f"""
                <div class="metric-container">
                    <h4>Risk Score</h4>
                    <div style="font-size: 1.5rem; color: #DC143C; font-weight: bold;">
                        {risk_profile.score}/10
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                level_name = str(risk_profile.level.name).replace('_', ' ').title() if hasattr(risk_profile.level, 'name') else f"Level {risk_profile.score}"
                st.markdown(f"""
                <div class="metric-container">
                    <h4>Risk Level</h4>
                    <div style="font-size: 1.2rem; color: #FFD700; font-weight: bold;">
                        {level_name}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="metric-container">
                    <h4>Trading Strategy</h4>
                    <div style="font-size: 1.2rem; color: #00FF41; font-weight: bold;">
                        {risk_profile.trading_strategy}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                st.markdown(f"""
                <div class="metric-container">
                    <h4>User Profile</h4>
                    <div style="font-size: 1.2rem; color: #00BFFF; font-weight: bold;">
                        {risk_profile.first_name} {risk_profile.last_name}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Positions Analysis
        self.render_positions_analysis(dashboard)

        # Quick Trading Panel
        self.render_quick_trading_panel(dashboard)

    def render_positions_analysis(self, dashboard):
        """Render enhanced positions analysis"""
        st.subheader("📊 Position Intelligence")
        positions_df = dashboard.get_positions()

        if not positions_df.empty:
            # Enhanced positions display with risk analysis
            if st.session_state.user_risk_profile:
                portfolio_risk = st.session_state.risk_profiler.calculate_portfolio_risk_score(
                    positions_df.to_dict('records')
                )

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Portfolio Risk Score", f"{portfolio_risk['score']}/10")
                with col2:
                    st.metric("Risk Level", portfolio_risk['level'])
                with col3:
                    st.metric("Diversification", f"{portfolio_risk['diversification']:.2%}")
                with col4:
                    st.metric("Open Positions", len(positions_df))

            # Positions table with enhanced styling
            st.dataframe(
                positions_df.style.format({
                    'Avg Entry': '${:.2f}',
                    'Current Price': '${:.2f}',
                    'Market Value': '${:,.2f}',
                    'Unrealized P/L': '${:,.2f}',
                    'Unrealized P/L %': '{:.2f}%'
                }).map(
                    lambda x: 'color: #00FF41; font-weight: bold' if isinstance(x, (int, float)) and x > 0
                    else 'color: #FF1744; font-weight: bold' if isinstance(x, (int, float)) and x < 0
                    else '',
                    subset=['Unrealized P/L', 'Unrealized P/L %']
                ),
                use_container_width=True
            )

            # Enhanced visualization
            pnl_chart = self.create_enhanced_pnl_chart(positions_df)
            if pnl_chart:
                st.plotly_chart(pnl_chart, use_container_width=True)

        else:
            st.markdown("""
            <div class="ai-section">
                <h3>📭 No Active Positions</h3>
                <p>Your portfolio is ready for new opportunities. Use the AI recommendations below to discover potential trades!</p>
            </div>
            """, unsafe_allow_html=True)

    def create_enhanced_pnl_chart(self, positions_df):
        """Create enhanced P&L chart with dark theme"""
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Portfolio Distribution', 'P&L Analysis'),
            specs=[[{'type': 'domain'}, {'type': 'bar'}]]
        )

        # Enhanced pie chart
        colors = ['#DC143C', '#FF1744', '#B71C1C', '#8B0000', '#660000']
        fig.add_trace(
            go.Pie(
                labels=positions_df['Symbol'],
                values=positions_df['Market Value'].abs(),
                name="Market Value",
                marker=dict(colors=colors),
                textfont=dict(color='white'),
                hole=0.3
            ),
            row=1, col=1
        )

        # Enhanced bar chart
        colors = ['#00FF41' if x >= 0 else '#FF1744' for x in positions_df['Unrealized P/L']]

        fig.add_trace(
            go.Bar(
                x=positions_df['Symbol'],
                y=positions_df['Unrealized P/L'],
                marker_color=colors,
                name="P&L",
                text=positions_df['Unrealized P/L'].apply(lambda x: f'${x:,.0f}'),
                textposition='auto',
                textfont=dict(color='white')
            ),
            row=1, col=2
        )

        fig.update_layout(
            title_text="Agent Chopra Portfolio Analysis",
            title_font=dict(color='#F0F6FC', size=20),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#F0F6FC'),
            height=500
        )

        fig.update_xaxes(showgrid=False, color='#F0F6FC')
        fig.update_yaxes(showgrid=True, gridcolor='#30363D', color='#F0F6FC')

        return fig

    def render_quick_trading_panel(self, dashboard):
        """Render quick trading panel"""
        with st.expander("🚀 Quick Strike Trading Panel", expanded=False):
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                symbol = st.text_input("Symbol", "AAPL", key="quick_symbol").upper()

            with col2:
                quantity = st.number_input("Quantity", min_value=1, value=1, key="quick_qty")

            with col3:
                side = st.selectbox("Side", ["BUY", "SELL"], key="quick_side")

            with col4:
                order_type = st.selectbox("Type", ["MARKET", "LIMIT"], key="quick_type")

            with col5:
                if order_type == "LIMIT":
                    limit_price = st.number_input("Limit Price", min_value=0.01, value=100.00, key="limit_price")
                else:
                    limit_price = None

            if st.button("Execute Trade", key="quick_trade", use_container_width=True):
                result = dashboard.place_order(symbol, quantity, side.lower(), order_type.lower(), limit_price)
                if result['success']:
                    st.success(f"✅ Order executed! ID: {result['order_id']}")
                else:
                    st.error(f"❌ Order failed: {result['error']}")

    def render_ai_features(self):
        """Render AI-powered features"""
        if not st.session_state.ai_assistant:
            st.markdown("""
            <div class="ai-section">
                <h3>🤖 Activate AI Intelligence</h3>
                <p>Enter your OpenAI API key in the sidebar to unlock advanced AI features:</p>
                <ul>
                    <li>🎯 Real-time trading insights</li>
                    <li>📊 Portfolio optimization</li>
                    <li>⚡ Risk-based recommendations</li>
                    <li>🧠 Intelligent chat assistant</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            return

        ai_assistant = st.session_state.ai_assistant

        # AI Chat Interface
        st.subheader("🤖 AI Trading Assistant")

        # Display chat history
        for i, (question, answer) in enumerate(st.session_state.chat_history[-5:]):  # Show last 5
            st.markdown(f"**You:** {question}")
            st.markdown(f'<div class="ai-response">🤖 **Agent Chopra AI:** {answer}</div>', unsafe_allow_html=True)

        # Chat input
        col1, col2 = st.columns([4, 1])
        with col1:
            question = st.text_area("Ask Agent Chopra anything about your trading:", height=100, key="ai_question")

        with col2:
            st.write("")  # Spacer
            st.write("")  # Spacer
            if st.button("Ask AI", use_container_width=True):
                if question.strip():
                    with st.spinner("🧠 Agent Chopra is analyzing..."):
                        answer = ai_assistant.query(question)
                        st.session_state.chat_history.append((question, answer))
                        st.rerun()

            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()

    def render_ai_insights(self):
        """Render AI insights"""
        if not st.session_state.ai_assistant:
            st.info("🤖 AI Assistant required for insights")
            return

        ai_assistant = st.session_state.ai_assistant

        # Initialize session state for AI insights
        if 'ai_insights' not in st.session_state:
            st.session_state.ai_insights = None
        if 'portfolio_analysis' not in st.session_state:
            st.session_state.portfolio_analysis = None

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Generate AI Insights", use_container_width=True, type="primary"):
                with st.spinner("🔬 Analyzing your trading patterns..."):
                    try:
                        insights = ai_assistant.get_trading_insights()
                        st.session_state.ai_insights = insights
                        st.success("✅ AI Insights generated successfully!")
                    except Exception as e:
                        st.error(f"❌ Error generating AI insights: {str(e)}")

        with col2:
            if st.button("Portfolio Analysis", use_container_width=True, type="primary"):
                with st.spinner("📈 Analyzing portfolio composition..."):
                    try:
                        analysis = ai_assistant.analyze_portfolio()
                        st.session_state.portfolio_analysis = analysis
                        st.success("✅ Portfolio analysis completed!")
                    except Exception as e:
                        st.error(f"❌ Error analyzing portfolio: {str(e)}")

        # Display results
        if st.session_state.ai_insights:
            st.markdown("### 🔬 AI Trading Insights")
            st.markdown(f'<div class="ai-response">{st.session_state.ai_insights}</div>', unsafe_allow_html=True)

        if st.session_state.portfolio_analysis:
            st.markdown("### 📈 Portfolio Analysis")
            st.markdown(f'<div class="ai-response">{st.session_state.portfolio_analysis}</div>', unsafe_allow_html=True)

    def render_risk_recommendations(self):
        """Render risk-based stock recommendations"""
        st.subheader("⚡ Agent Chopra Recommendations")

        if not st.session_state.user_risk_profile:
            st.warning("🎯 Complete risk assessment to get personalized recommendations")
            return

        risk_profile = st.session_state.user_risk_profile
        profiler = st.session_state.risk_profiler

        # Get current portfolio
        dashboard = st.session_state.trading_dashboard
        positions_df = dashboard.get_positions()
        current_portfolio = positions_df.to_dict('records') if not positions_df.empty else []

        if st.button("Get AI Recommendations", use_container_width=True):
            with st.spinner("🎯 Generating personalized recommendations..."):
                recommendations = profiler.get_stock_recommendations(
                    risk_profile, current_portfolio
                )

                if recommendations:
                    st.subheader(f"🎯 Recommendations for Risk Level {risk_profile.score}/10")

                    for i, rec in enumerate(recommendations[:5], 1):
                        with st.expander(f"#{i} {rec.symbol} - {rec.company_name} (Strength: {rec.recommendation_strength:.1%})"):
                            col1, col2, col3 = st.columns(3)

                            with col1:
                                st.metric("Current Price", f"${rec.current_price:.2f}")
                                st.metric("Target Price", f"${rec.target_price:.2f}")

                            with col2:
                                st.metric("Risk Rating", f"{rec.risk_rating}/10")
                                st.metric("Sector", rec.sector.value.title())

                            with col3:
                                upside = ((rec.target_price / rec.current_price) - 1) * 100
                                st.metric("Potential Upside", f"{upside:.1f}%")
                                st.metric("Target Allocation", f"{rec.target_allocation:.1%}")

                            st.write(f"**Reasoning:** {rec.reasoning}")

                            if st.button(f"🚀 Trade {rec.symbol}", key=f"trade_{rec.symbol}"):
                                st.info(f"Use the Quick Trading Panel to execute trades for {rec.symbol}")

                else:
                    st.info("No suitable recommendations found for your risk profile.")

    def run(self):
        """Main application entry point"""
        self.render_header()

        # Sidebar
        refresh_rate = self.render_sidebar()

        # Main content tabs
        if st.session_state.ai_assistant:
            if ADVANCED_FEATURES_AVAILABLE:
                tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
                    "Command Center",
                    "AI Assistant",
                    "AI Insights",
                    "Recommendations",
                    "Daily P&L",
                    "Watchlist",
                    "Market News",
                    "Research",
                    "Voice Assistant"
                ])
            else:
                tab1, tab2, tab3, tab4, tab5 = st.tabs([
                    "Command Center",
                    "AI Assistant",
                    "AI Insights",
                    "Recommendations",
                    "Risk Profile"
                ])
        else:
            tab1, tab2 = st.tabs(["Command Center", "Setup"])

            with tab2:
                st.markdown("""
                <div class="ai-section">
                    <h3>🔥 Activate Agent Chopra Intelligence</h3>
                    <p>Unlock the full power of AI-driven trading insights!</p>
                </div>
                """, unsafe_allow_html=True)

                st.info("💡 **Enter your OpenAI API key in the sidebar to unlock:**")
                st.markdown("""
                **🚀 Advanced Features:**
                - 🎯 Real-time portfolio analysis
                - 🧠 Intelligent trading insights
                - ⚡ Risk-optimized recommendations
                - 🤖 Interactive AI chat assistant
                - 📊 Advanced risk profiling

                **How to get started:**
                1. Get OpenAI API key from https://platform.openai.com/
                2. Enter it in the sidebar
                3. Complete your risk assessment
                4. Start trading with AI guidance!
                """)

        # Render tab content
        with tab1:
            self.render_trading_dashboard()

        if st.session_state.ai_assistant:
            with tab2:
                self.render_ai_features()

            with tab3:
                self.render_ai_insights()

            with tab4:
                self.render_risk_recommendations()

            with tab5:
                if ADVANCED_FEATURES_AVAILABLE:
                    create_daily_pnl_dashboard(st.session_state.alpha_vantage_api, st.session_state.market_intelligence)
                else:
                    if st.session_state.user_risk_profile:
                        profile = st.session_state.user_risk_profile
                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown(f"""
                            <div class="risk-card">
                                <h3>Your Risk Profile</h3>
                                <div class="risk-score">{profile.score}/10</div>
                                <div style="text-align: center; margin: 1rem 0;">
                                    <strong>{profile.level.value.replace('_', ' ').title()}</strong>
                                </div>
                                <p>{profile.description}</p>
                            </div>
                            """, unsafe_allow_html=True)

                        with col2:
                            st.subheader("📊 Recommended Allocation")
                            allocation_df = pd.DataFrame(
                                list(profile.allocation.items()),
                                columns=['Asset Class', 'Allocation %']
                            )
                            # Create enhanced color palette for better visualization
                            color_palette = [
                                '#DC143C',  # Primary red
                                '#FF6B6B',  # Light red
                                '#4ECDC4',  # Teal
                                '#45B7D1',  # Blue
                                '#96CEB4',  # Green
                                '#FECA57',  # Yellow
                                '#FF9FF3',  # Pink
                                '#54A0FF',  # Light blue
                                '#5F27CD',  # Purple
                                '#00D2D3'   # Cyan
                            ]

                            fig = px.pie(
                                allocation_df,
                                values='Allocation %',
                                names='Asset Class',
                                color_discrete_sequence=color_palette,
                                hover_data=['Allocation %'],
                                hole=0.3  # Create donut chart for better visual appeal
                            )
                            fig.update_traces(
                                textposition='inside',
                                textinfo='percent+label',
                                hovertemplate='<b>%{label}</b><br>' +
                                            'Allocation: %{value}%<br>' +
                                            '<extra></extra>'
                            )
                            fig.update_layout(
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                font=dict(color='white', size=12),
                                showlegend=True,
                                legend=dict(
                                    orientation="v",
                                    yanchor="middle",
                                    y=0.5,
                                    xanchor="left",
                                    x=1.05
                                ),
                                margin=dict(t=50, b=50, l=50, r=150)
                            )
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        self.show_risk_assessment()

            # Advanced feature tabs (only available when APIs are configured)
            if ADVANCED_FEATURES_AVAILABLE:
                with tab6:  # Watchlist
                    create_stock_watchlist(st.session_state.alpha_vantage_api, st.session_state.market_intelligence)

                with tab7:  # Market News
                    create_market_news_section(st.session_state.alpha_vantage_api)

                with tab8:  # Research
                    create_market_research_dashboard(st.session_state.brave_search_api, st.session_state.market_researcher)

                with tab9:  # Voice Assistant
                    create_voice_interface()

        # Footer
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.caption(f"🕐 Last updated: {datetime.now().strftime('%H:%M:%S')}")

        with col2:
            st.caption("🔄 Auto-refresh active" if refresh_rate > 0 else "🔄 Manual refresh")

        with col3:
            st.caption("🔥 Paper Trading Mode")

        with col4:
            if st.session_state.ai_assistant:
                st.caption("🤖 Agent Chopra: ACTIVE")
            else:
                st.caption("🤖 Agent Chopra: STANDBY")

def main():
    """Entry point"""
    app = AgentChopra()
    app.run()

if __name__ == "__main__":
    main()