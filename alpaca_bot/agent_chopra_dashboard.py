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
    from google_news_integration import (
        GoogleNewsAPI, MarketNewsHub,
        create_google_news_dashboard, create_stock_news_widget, init_google_news
    )
    from voice_integration import (
        VoiceAssistant, create_voice_interface, create_voice_quick_actions
    )
    from visual_analytics import create_visual_analytics_dashboard
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
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Open+Sans:wght@300;400;500;600;700&display=swap');

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
        font-family: 'Open Sans', sans-serif;
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
        padding: 1.2rem;
        margin: 1rem 0;
        font-family: 'Open Sans', sans-serif;
        box-shadow: 0 0 15px rgba(220, 20, 60, 0.2);
        line-height: 1.6;
    }

    .ai-response p {
        margin: 0.8rem 0 !important;
        line-height: 1.6 !important;
    }

    .ai-response ul, .ai-response ol {
        margin: 0.5rem 0 !important;
        padding-left: 1.5rem !important;
    }

    .ai-response li {
        margin: 0.3rem 0 !important;
        line-height: 1.5 !important;
    }

    .ai-response strong {
        color: var(--primary-red) !important;
    }

    .ai-response h1, .ai-response h2, .ai-response h3, .ai-response h4 {
        margin: 1rem 0 0.5rem 0 !important;
        color: var(--accent-gold) !important;
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

    /* Additional dataframe dark theme enforcement */
    .stDataFrame div[data-testid="stDataFrame"] {
        background: #161B22 !important;
        color: #E6E6E6 !important;
    }

    .stDataFrame div[data-testid="stDataFrame"] div {
        background: #161B22 !important;
        color: #E6E6E6 !important;
    }

    .stDataFrame iframe {
        background: #161B22 !important;
    }

    /* Force dark theme on all dataframe elements */
    [data-testid="stDataFrame"] * {
        background: #161B22 !important;
        color: #FFFFFF !important;
    }

    /* Additional specific targeting for cells */
    [data-testid="stDataFrame"] div div div {
        color: #FFFFFF !important;
    }

    [data-testid="stDataFrame"] span {
        color: #FFFFFF !important;
    }

    [data-testid="stDataFrame"] p {
        color: #FFFFFF !important;
    }

    /* Target the actual data cells more specifically */
    [data-testid="stDataFrame"] [role="gridcell"] {
        color: #FFFFFF !important;
        background: #161B22 !important;
    }

    [data-testid="stDataFrame"] [role="columnheader"] {
        color: #FFFFFF !important;
        background: #21262D !important;
    }

    /* Specific styling for styled dataframes */
    .stDataFrame .dataframe {
        background: #161B22 !important;
        color: #E6E6E6 !important;
        border: 1px solid #DC143C !important;
    }

    .stDataFrame .dataframe th {
        background: #21262D !important;
        color: #E6E6E6 !important;
        border-bottom: 2px solid #DC143C !important;
    }

    .stDataFrame .dataframe td {
        background: #161B22 !important;
        color: #FFFFFF !important;
        border-bottom: 1px solid #30363D !important;
    }

    /* Additional targeting for Streamlit's internal classes */
    .stDataFrame [data-testid="stDataFrame"] .element-container {
        color: #FFFFFF !important;
    }

    /* Target any text elements inside dataframes */
    .stDataFrame [data-testid="stDataFrame"] .row-widget {
        color: #FFFFFF !important;
    }

    /* Force white text on all table elements */
    .stDataFrame table * {
        color: #FFFFFF !important;
    }

    /* Override any inherited styles */
    .stDataFrame .css-1d391kg, .stDataFrame .css-1v0mbdj, .stDataFrame .e1tzin5v0 {
        color: #FFFFFF !important;
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

    /* Enhanced Selectbox styling for better visibility */
    .stSelectbox > div > div {
        padding: 8px 12px !important;
        border-radius: 6px !important;
        background: var(--card-bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
    }

    /* Enhanced Selectbox styling - comprehensive coverage */
    div[data-testid="stSelectbox"] > div > div {
        background: var(--card-bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
    }

    /* Selectbox input field */
    div[data-testid="stSelectbox"] input {
        color: var(--text-primary) !important;
        background: var(--card-bg) !important;
    }

    /* Selectbox selected value display */
    div[data-testid="stSelectbox"] > div > div > div {
        background: var(--card-bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
    }

    /* Selected option text - all variations */
    div[data-testid="stSelectbox"] > div > div > div > div,
    div[data-testid="stSelectbox"] span,
    .stSelectbox > div > div > div > div {
        color: var(--text-primary) !important;
        background: transparent !important;
    }

    /* Dropdown options menu */
    div[data-testid="stSelectbox"] ul,
    .stSelectbox ul {
        background: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5) !important;
    }

    /* Individual dropdown options */
    div[data-testid="stSelectbox"] li,
    .stSelectbox li {
        color: var(--text-primary) !important;
        background: var(--card-bg) !important;
        padding: 8px 12px !important;
    }

    /* Dropdown option hover */
    div[data-testid="stSelectbox"] li:hover,
    .stSelectbox li:hover {
        background: rgba(220, 20, 60, 0.1) !important;
        color: var(--text-primary) !important;
    }

    /* Selectbox arrow icon */
    div[data-testid="stSelectbox"] svg {
        fill: var(--text-primary) !important;
    }

    /* Additional fallback selectors for newer Streamlit versions */
    .st-selectbox,
    [data-baseweb="select"] {
        background: var(--card-bg) !important;
        color: var(--text-primary) !important;
    }

    [data-baseweb="select"] > div {
        background: var(--card-bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
    }

    [data-baseweb="menu"] {
        background: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
    }

    [data-baseweb="menu"] li {
        color: var(--text-primary) !important;
        background: var(--card-bg) !important;
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

    /* Enhanced Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        background: linear-gradient(135deg, #1a1a1a 0%, #2d1b1b 100%);
        border-radius: 12px;
        padding: 8px;
        border: 2px solid #DC143C;
        margin-bottom: 20px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 60px !important;
        min-width: 160px !important;
        background: linear-gradient(135deg, #161B22 0%, #0D1117 100%);
        border-radius: 8px !important;
        margin: 2px;
        padding: 0 20px !important;
        border: 1px solid #30363D !important;
        position: relative;
        transition: all 0.3s ease !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        text-align: center !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #DC143C 0%, #8B0000 100%) !important;
        border: 1px solid #DC143C !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(220, 20, 60, 0.3) !important;
        color: white !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #DC143C 0%, #8B0000 100%) !important;
        color: white !important;
        border: 2px solid #FFD700 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 15px rgba(255, 215, 0, 0.4) !important;
        font-weight: 700 !important;
    }

    .stTabs [aria-selected="true"]::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 50%;
        transform: translateX(-50%);
        width: 40px;
        height: 3px;
        background: #FFD700;
        border-radius: 2px;
    }

    .stTabs [data-baseweb="tab"] p {
        margin: 0 !important;
        font-size: 16px !important;
        font-weight: inherit !important;
        text-align: center !important;
        white-space: nowrap !important;
    }

    /* Tab content styling */
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 20px !important;
        background: transparent !important;
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

            # Initialize Google News API
            if 'google_news_api' not in st.session_state:
                st.session_state.google_news_api = init_google_news()

            if 'market_news_hub' not in st.session_state:
                st.session_state.market_news_hub = MarketNewsHub(st.session_state.google_news_api)

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

        # Auto-Trading Mode
        st.sidebar.subheader("🤖 Auto-Trading Mode")

        # Initialize auto-trading state
        if 'auto_trading_enabled' not in st.session_state:
            st.session_state.auto_trading_enabled = False
        if 'auto_trading_active' not in st.session_state:
            st.session_state.auto_trading_active = False

        # Auto-Trading Toggle
        auto_trading_enabled = st.sidebar.checkbox(
            "🔥 Enable Auto-Trading",
            value=st.session_state.auto_trading_enabled,
            help="Enable autonomous trading based on AI recommendations"
        )
        st.session_state.auto_trading_enabled = auto_trading_enabled

        if auto_trading_enabled:
            # Auto-Trading Controls
            col1, col2 = st.sidebar.columns(2)

            with col1:
                if st.button("▶️ START", type="primary", use_container_width=True):
                    st.session_state.auto_trading_active = True
                    st.sidebar.success("🔥 Auto-Trading ACTIVE!")

            with col2:
                if st.button("⏹️ STOP", use_container_width=True):
                    st.session_state.auto_trading_active = False
                    st.sidebar.warning("⏸️ Auto-Trading STOPPED")

            # Auto-Trading Settings
            if st.session_state.auto_trading_active:
                st.sidebar.markdown("**⚙️ Auto-Trading Settings**")

                max_position_size = st.sidebar.slider(
                    "Max Position Size (%)",
                    min_value=1,
                    max_value=50,
                    value=10,
                    help="Maximum % of portfolio per trade"
                )

                confidence_threshold = st.sidebar.slider(
                    "Confidence Threshold",
                    min_value=0.5,
                    max_value=1.0,
                    value=0.75,
                    step=0.05,
                    help="Minimum confidence for auto-execution"
                )

                max_daily_trades = st.sidebar.number_input(
                    "Max Daily Trades",
                    min_value=1,
                    max_value=20,
                    value=5,
                    help="Maximum trades per day"
                )

                # Store settings in session state
                st.session_state.auto_trading_settings = {
                    'max_position_size': max_position_size,
                    'confidence_threshold': confidence_threshold,
                    'max_daily_trades': max_daily_trades
                }

                # Status indicator
                st.sidebar.markdown("""
                <div style='background: linear-gradient(135deg, #DC143C 0%, #8B0000 100%);
                            padding: 10px; border-radius: 8px; text-align: center; margin-top: 10px;'>
                    <strong style='color: white;'>🔥 LIVE AUTO-TRADING</strong>
                </div>
                """, unsafe_allow_html=True)

        # Auto-refresh settings
        st.sidebar.subheader("🔄 Auto-refresh")
        refresh_options = {
            "Off": 0,
            "10 seconds": 10,
            "30 seconds": 30,
            "1 minute": 60,
            "5 minutes": 300
        }

        selected_refresh = st.sidebar.selectbox(
            "Refresh interval",
            list(refresh_options.keys()),
            index=2  # Default to "30 seconds"
        )
        refresh_rate = refresh_options[selected_refresh]

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
                status_text = "Active" if account_data['status'] == 'ACTIVE' else account_data['status']
                st.markdown(f"""
                <div class="metric-container">
                    <h4>Account Status</h4>
                    <div style="font-size: 1.5rem; color: #00FF41; font-weight: bold;">
                        {status_text}
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
                    <div style="font-size: 1.5rem; color: #FFD700; font-weight: bold;">
                        {level_name}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="metric-container">
                    <h4>Trading Strategy</h4>
                    <div style="font-size: 1.5rem; color: #00FF41; font-weight: bold;">
                        {risk_profile.trading_strategy}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                st.markdown(f"""
                <div class="metric-container">
                    <h4>User Profile</h4>
                    <div style="font-size: 1.5rem; color: #00BFFF; font-weight: bold;">
                        {risk_profile.first_name} {risk_profile.last_name}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Positions Analysis
        self.render_positions_analysis(dashboard)

        # Quick Trading Panel
        self.render_quick_trading_panel(dashboard)

    def render_positions_analysis(self, dashboard):
        """Render simplified position intelligence"""
        st.subheader("📊 Position Intelligence")

        try:
            positions_df = dashboard.get_positions()

            if not positions_df.empty:
                # Basic portfolio metrics
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    total_positions = len(positions_df)
                    st.metric("Open Positions", total_positions)

                with col2:
                    total_value = positions_df['Market Value'].sum() if 'Market Value' in positions_df.columns else 0
                    st.metric("Total Value", f"${total_value:,.2f}")

                with col3:
                    total_pnl = positions_df['Unrealized P/L'].sum() if 'Unrealized P/L' in positions_df.columns else 0
                    st.metric("Total P/L", f"${total_pnl:,.2f}")

                with col4:
                    avg_pnl = (positions_df['Unrealized P/L %'].mean() if 'Unrealized P/L %' in positions_df.columns else 0)
                    st.metric("Avg P/L %", f"{avg_pnl:.2f}%")

                st.markdown("---")

                # Simple table display
                st.markdown("**Position Details:**")

                # Create a clean display dataframe
                if len(positions_df) > 0:
                    # Select only the most important columns
                    display_cols = []
                    for col in ['Symbol', 'Quantity', 'Side', 'Avg Entry', 'Current Price', 'Market Value', 'Unrealized P/L', 'Unrealized P/L %']:
                        if col in positions_df.columns:
                            display_cols.append(col)

                    if display_cols:
                        clean_df = positions_df[display_cols].copy()

                        # Format numeric columns
                        for col in clean_df.columns:
                            if 'Price' in col or 'Value' in col:
                                clean_df[col] = clean_df[col].apply(lambda x: f"${x:.2f}" if pd.notna(x) else "N/A")
                            elif 'P/L %' in col:
                                clean_df[col] = clean_df[col].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else "N/A")
                            elif 'P/L' in col and 'P/L %' not in col:
                                clean_df[col] = clean_df[col].apply(lambda x: f"${x:.2f}" if pd.notna(x) else "N/A")

                        # Display the table with better formatting
                        st.table(clean_df)
                    else:
                        st.table(positions_df)

            else:
                st.info("🔍 No active positions found. Ready to start trading!")

        except Exception as e:
            st.error(f"Error loading positions: {str(e)}")
            st.info("Please check your Alpaca API connection.")

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

        # Initialize voice assistant for TTS
        if 'voice_assistant' not in st.session_state:
            st.session_state.voice_assistant = VoiceAssistant()

        voice_assistant = st.session_state.voice_assistant

        # Display chat history with TTS buttons
        for i, (question, answer) in enumerate(st.session_state.chat_history[-5:]):  # Show last 5
            st.markdown(f"**You:** {question}")

            # Create columns for AI response and TTS button
            col_response, col_tts = st.columns([5, 1])

            with col_response:
                st.markdown(f'<div class="ai-response">🤖 **Agent Chopra AI:** {answer}</div>', unsafe_allow_html=True)

            with col_tts:
                if st.button("🔊", key=f"tts_chat_{i}", help="Listen to response", use_container_width=True):
                    with st.spinner("🎵 Converting to speech..."):
                        voice_assistant.speak_text(f"Agent Chopra says: {answer}")

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
                        st.session_state.ai_insights_time = datetime.now()
                        st.success("✅ AI Insights generated successfully!")
                    except Exception as e:
                        st.error(f"❌ Error generating AI insights: {str(e)}")

        with col2:
            if st.button("Portfolio Analysis", use_container_width=True, type="primary"):
                with st.spinner("📈 Analyzing portfolio composition..."):
                    try:
                        analysis = ai_assistant.analyze_portfolio()
                        st.session_state.portfolio_analysis = analysis
                        st.session_state.portfolio_analysis_time = datetime.now()
                        st.success("✅ Portfolio analysis completed!")
                    except Exception as e:
                        st.error(f"❌ Error analyzing portfolio: {str(e)}")

        # Initialize voice assistant for TTS
        if 'voice_assistant' not in st.session_state:
            st.session_state.voice_assistant = VoiceAssistant()

        voice_assistant = st.session_state.voice_assistant

        # Display results with timestamps and persistence
        if st.session_state.ai_insights:
            insights_time = getattr(st.session_state, 'ai_insights_time', datetime.now())
            time_diff = (datetime.now() - insights_time).seconds

            col_title, col_tts = st.columns([4, 1])
            with col_title:
                st.markdown("### 🔬 AI Trading Insights")
                st.caption(f"Generated {time_diff}s ago")

            with col_tts:
                if st.button("🔊 Listen to Insights", key="tts_insights", use_container_width=True):
                    with st.spinner("🎵 Converting insights to speech..."):
                        voice_assistant.speak_text(f"Here are your AI trading insights: {st.session_state.ai_insights}")

            # Use expander to prevent content from disappearing during auto-refresh
            with st.expander("📈 View Latest AI Insights", expanded=True):
                st.markdown(f'<div class="ai-response">{st.session_state.ai_insights}</div>', unsafe_allow_html=True)

        if st.session_state.portfolio_analysis:
            analysis_time = getattr(st.session_state, 'portfolio_analysis_time', datetime.now())
            time_diff = (datetime.now() - analysis_time).seconds

            col_title2, col_tts2 = st.columns([4, 1])
            with col_title2:
                st.markdown("### 📊 Portfolio Analysis")
                st.caption(f"Generated {time_diff}s ago")

            with col_tts2:
                if st.button("🔊 Listen to Analysis", key="tts_portfolio", use_container_width=True):
                    with st.spinner("🎵 Converting analysis to speech..."):
                        voice_assistant.speak_text(f"Here is your portfolio analysis: {st.session_state.portfolio_analysis}")

            # Use expander to prevent content from disappearing during auto-refresh
            with st.expander("📊 View Portfolio Analysis", expanded=True):
                st.markdown(f'<div class="ai-response">{st.session_state.portfolio_analysis}</div>', unsafe_allow_html=True)

    def render_watchlist_management(self):
        """Render enhanced watchlist management"""
        st.subheader("📋 My Watchlist")

        # Initialize watchlist in session state
        if 'user_watchlist' not in st.session_state:
            st.session_state.user_watchlist = []

        # Add new stock section
        st.markdown("### ➕ Add Stock to Watchlist")
        col1, col2 = st.columns([3, 1])

        with col1:
            new_stock = st.text_input(
                "Enter Stock Symbol (e.g., AAPL, TSLA, MSFT)",
                placeholder="Stock symbol...",
                key="watchlist_input"
            ).upper()

        with col2:
            if st.button("➕ Add", type="primary", use_container_width=True):
                if new_stock and len(new_stock) > 0:
                    if new_stock not in st.session_state.user_watchlist:
                        st.session_state.user_watchlist.append(new_stock)
                        st.success(f"✅ {new_stock} added to watchlist!")
                        st.rerun()
                    else:
                        st.warning(f"⚠️ {new_stock} is already in your watchlist!")
                else:
                    st.error("Please enter a valid stock symbol!")

        st.markdown("---")

        # Display current watchlist
        if st.session_state.user_watchlist:
            st.markdown(f"### 👁️ Your Watchlist ({len(st.session_state.user_watchlist)} stocks)")

            # Create a more interactive watchlist display
            for i, stock in enumerate(st.session_state.user_watchlist):
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])

                with col1:
                    st.markdown(f"**{stock}**")

                with col2:
                    # Try to get current price (placeholder for now)
                    st.markdown("$---")

                with col3:
                    # Status placeholder
                    st.markdown("📊 Watching")

                with col4:
                    if st.button("🗑️", key=f"remove_{stock}_{i}", help=f"Remove {stock}"):
                        st.session_state.user_watchlist.remove(stock)
                        st.success(f"🗑️ {stock} removed from watchlist!")
                        st.rerun()

            # Bulk actions
            st.markdown("---")
            col1, col2 = st.columns(2)

            with col1:
                if st.button("🗑️ Clear All", use_container_width=True):
                    st.session_state.user_watchlist = []
                    st.success("🗑️ Watchlist cleared!")
                    st.rerun()

            with col2:
                if st.button("💾 Export List", use_container_width=True):
                    watchlist_text = "\n".join(st.session_state.user_watchlist)
                    st.text_area("Your Watchlist:", watchlist_text, height=100)

        else:
            st.info("📋 Your watchlist is empty. Add some stocks to get started!")

        # Quick add from popular stocks
        st.markdown("### 🔥 Quick Add Popular Stocks")
        popular_stocks = ['AAPL', 'TSLA', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'NFLX']

        cols = st.columns(4)
        for i, stock in enumerate(popular_stocks):
            col_idx = i % 4
            with cols[col_idx]:
                if st.button(f"➕ {stock}", key=f"quick_add_{stock}", use_container_width=True):
                    if stock not in st.session_state.user_watchlist:
                        st.session_state.user_watchlist.append(stock)
                        st.success(f"✅ {stock} added!")
                        st.rerun()
                    else:
                        st.warning(f"{stock} already in watchlist!")

    def render_risk_recommendations(self):
        """Render risk-aware stock recommendations based on user profile"""
        # Get user's risk profile
        user_risk_level = None
        if st.session_state.user_risk_profile:
            # RiskProfile object has 'score' attribute (1-10)
            user_risk_level = getattr(st.session_state.user_risk_profile, 'score', None)

        st.markdown("""
        <div style='background: linear-gradient(135deg, #1a1a1a 0%, #2d1b1b 100%);
                    padding: 20px; border-radius: 15px; margin-bottom: 20px;
                    border: 2px solid #DC143C;'>
            <h2 style='color: #DC143C; margin: 0; text-align: center;'>
                ⚡ AGENT CHOPRA RECOMMENDATIONS
            </h2>
            <p style='color: #888; text-align: center; margin: 5px 0 0 0;'>
                AI-Powered Stock Analysis Tailored to Your Risk Profile
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Display current risk profile or prompt to set one
        if not user_risk_level:
            st.warning("⚠️ Please complete your risk assessment first to get personalized recommendations!")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("📊 Complete Risk Assessment", type="primary", use_container_width=True):
                    st.session_state.show_risk_assessment_inline = True
                    st.rerun()

            with col2:
                st.info("💡 Go to 'Command Center' tab to complete your risk profile")

            # Show inline risk assessment if requested
            if st.session_state.get('show_risk_assessment_inline', False):
                st.markdown("---")
                st.markdown("### 📊 Quick Risk Assessment")
                self.show_risk_assessment()

                if st.button("✅ Assessment Complete - View Recommendations", type="primary"):
                    st.session_state.show_risk_assessment_inline = False
                    st.rerun()

            return

        # Risk-based stock database
        all_stocks = [
            # Conservative (Risk 1-3)
            {"symbol": "JNJ", "company": "Johnson & Johnson", "price": 160.00, "target": 175.00, "risk": 2, "strength": 0.85, "sector": "Healthcare"},
            {"symbol": "PG", "company": "Procter & Gamble", "price": 150.00, "target": 165.00, "risk": 2, "strength": 0.80, "sector": "Consumer Staples"},
            {"symbol": "KO", "company": "Coca-Cola", "price": 58.00, "target": 65.00, "risk": 2, "strength": 0.75, "sector": "Consumer Staples"},
            {"symbol": "MSFT", "company": "Microsoft Corp.", "price": 415.00, "target": 470.00, "risk": 3, "strength": 0.92, "sector": "Technology"},
            {"symbol": "JPM", "company": "JPMorgan Chase", "price": 165.00, "target": 185.00, "risk": 3, "strength": 0.78, "sector": "Financial"},

            # Moderate (Risk 4-6)
            {"symbol": "AAPL", "company": "Apple Inc.", "price": 175.00, "target": 200.00, "risk": 4, "strength": 0.88, "sector": "Technology"},
            {"symbol": "V", "company": "Visa Inc.", "price": 250.00, "target": 280.00, "risk": 4, "strength": 0.82, "sector": "Financial"},
            {"symbol": "GOOGL", "company": "Alphabet Inc.", "price": 140.00, "target": 165.00, "risk": 5, "strength": 0.85, "sector": "Technology"},
            {"symbol": "UNH", "company": "UnitedHealth Group", "price": 520.00, "target": 580.00, "risk": 5, "strength": 0.79, "sector": "Healthcare"},
            {"symbol": "AMZN", "company": "Amazon.com Inc.", "price": 145.00, "target": 175.00, "risk": 6, "strength": 0.74, "sector": "Consumer Discretionary"},

            # Aggressive (Risk 7-10)
            {"symbol": "NVDA", "company": "NVIDIA Corp.", "price": 875.00, "target": 1100.00, "risk": 7, "strength": 0.89, "sector": "Technology"},
            {"symbol": "TSLA", "company": "Tesla Inc.", "price": 240.00, "target": 300.00, "risk": 8, "strength": 0.68, "sector": "Automotive"},
            {"symbol": "META", "company": "Meta Platforms", "price": 320.00, "target": 400.00, "risk": 8, "strength": 0.71, "sector": "Technology"},
            {"symbol": "SHOP", "company": "Shopify Inc.", "price": 65.00, "target": 90.00, "risk": 9, "strength": 0.63, "sector": "E-commerce"},
            {"symbol": "PLTR", "company": "Palantir Technologies", "price": 18.00, "target": 28.00, "risk": 10, "strength": 0.55, "sector": "Technology"}
        ]

        # Filter stocks based on user's risk profile
        risk_tolerance = 2  # Allow some variance

        if user_risk_level <= 3:  # Conservative
            filtered_stocks = [s for s in all_stocks if s['risk'] <= user_risk_level + 1]
            risk_category = "Conservative"
        elif user_risk_level <= 6:  # Moderate
            filtered_stocks = [s for s in all_stocks if user_risk_level - 2 <= s['risk'] <= user_risk_level + 2]
            risk_category = "Moderate"
        else:  # Aggressive
            filtered_stocks = [s for s in all_stocks if s['risk'] >= user_risk_level - 2]
            risk_category = "Aggressive"

        # Show current risk profile and sector filtering
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Your Risk Level", f"{user_risk_level}/10")
        with col2:
            st.metric("Risk Category", risk_category)
        with col3:
            st.metric("Available Stocks", len(filtered_stocks))

        # Sector/Segment filtering
        available_sectors = list(set([stock['sector'] for stock in filtered_stocks]))
        available_sectors.insert(0, "All Sectors")

        with col4:
            selected_sector = st.selectbox(
                "🏢 Filter by Sector:",
                available_sectors,
                key="sector_filter"
            )

        # Apply sector filtering
        if selected_sector != "All Sectors":
            filtered_stocks = [s for s in filtered_stocks if s['sector'] == selected_sector]

        # Update metrics after sector filtering
        if selected_sector != "All Sectors":
            col3.metric("Filtered Stocks", len(filtered_stocks))

        # Check if we have any stocks after filtering
        if not filtered_stocks:
            st.warning(f"⚠️ No stocks available for {risk_category} risk level in {selected_sector if selected_sector != 'All Sectors' else 'any'} sector.")
            st.info("💡 Try adjusting your risk profile or selecting a different sector.")
            return

        import plotly.graph_objects as go
        import plotly.express as px
        import pandas as pd
        import numpy as np

        df = pd.DataFrame(filtered_stocks)
        df['upside'] = ((df['target'] / df['price']) - 1) * 100
        df['market_cap'] = np.random.uniform(500, 3000, len(df))  # Billions

        # Visual Risk Profile Display
        st.markdown("### 📊 Your Risk Profile Visualization")

        # Risk gauge chart
        risk_gauge_fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = user_risk_level,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Risk Level", 'font': {'size': 20, 'color': '#F0F6FC'}},
            delta = {'reference': 5, 'increasing': {'color': "#DC143C"}, 'decreasing': {'color': "#00FF41"}},
            gauge = {
                'axis': {'range': [None, 10], 'tickcolor': "#F0F6FC", 'tickfont': {'color': '#F0F6FC'}},
                'bar': {'color': "#DC143C"},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "#F0F6FC",
                'steps': [
                    {'range': [0, 3], 'color': "#00FF41"},
                    {'range': [3, 6], 'color': "#FFD700"},
                    {'range': [6, 10], 'color': "#FF1744"}],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': user_risk_level}}))

        risk_gauge_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "#F0F6FC"},
            height=300
        )

        col1, col2 = st.columns([1, 2])
        with col1:
            st.plotly_chart(risk_gauge_fig, use_container_width=True)

        with col2:
            # Risk profile recommendations
            if user_risk_level <= 3:
                st.markdown("""
                <div style='background: linear-gradient(135deg, #1a4d1a 0%, #0d2b0d 100%);
                            padding: 15px; border-radius: 10px; border: 1px solid #00FF41;'>
                    <h4 style='color: #00FF41; margin: 0;'>🛡️ Conservative Profile</h4>
                    <p style='color: #ccc; margin: 5px 0;'>
                        • Focus on dividend-paying blue chips<br>
                        • Low volatility, stable returns<br>
                        • Maximum position size: 5-10%<br>
                        • Recommended: Healthcare, Consumer Staples
                    </p>
                </div>
                """, unsafe_allow_html=True)
            elif user_risk_level <= 6:
                st.markdown("""
                <div style='background: linear-gradient(135deg, #4d4d1a 0%, #2b2b0d 100%);
                            padding: 15px; border-radius: 10px; border: 1px solid #FFD700;'>
                    <h4 style='color: #FFD700; margin: 0;'>⚖️ Moderate Profile</h4>
                    <p style='color: #ccc; margin: 5px 0;'>
                        • Balanced growth and income<br>
                        • Moderate volatility acceptable<br>
                        • Maximum position size: 10-15%<br>
                        • Recommended: Technology, Financials
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style='background: linear-gradient(135deg, #4d1a1a 0%, #2b0d0d 100%);
                            padding: 15px; border-radius: 10px; border: 1px solid #FF1744;'>
                    <h4 style='color: #FF1744; margin: 0;'>🚀 Aggressive Profile</h4>
                    <p style='color: #ccc; margin: 5px 0;'>
                        • High growth potential focus<br>
                        • High volatility acceptable<br>
                        • Maximum position size: 15-25%<br>
                        • Recommended: Tech Growth, Emerging Markets
                    </p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")

        # Show sector breakdown with visual chart
        if selected_sector == "All Sectors":
            st.markdown("### 🏢 Sector Allocation Visualization")

            sector_counts = {}
            for stock in filtered_stocks:
                sector = stock['sector']
                sector_counts[sector] = sector_counts.get(sector, 0) + 1

            # Create pie chart for sector distribution
            sector_pie_fig = go.Figure(data=[go.Pie(
                labels=list(sector_counts.keys()),
                values=list(sector_counts.values()),
                hole=.3,
                textfont_size=12,
                marker=dict(
                    colors=['#DC143C', '#00FF41', '#FFD700', '#1E90FF', '#FF69B4', '#32CD32', '#FF8C00', '#9370DB'],
                    line=dict(color='#000000', width=2)
                )
            )])

            sector_pie_fig.update_layout(
                title={'text': f"Available Stocks by Sector ({risk_category} Risk)", 'font': {'color': '#F0F6FC'}},
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={'color': "#F0F6FC"},
                height=400,
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.05
                )
            )

            col1, col2 = st.columns([2, 1])
            with col1:
                st.plotly_chart(sector_pie_fig, use_container_width=True)

            with col2:
                st.markdown("**📊 Sector Breakdown:**")
                for sector, count in sector_counts.items():
                    percentage = (count / len(filtered_stocks)) * 100
                    st.metric(f"{sector}", f"{count} stocks", f"{percentage:.1f}%")

        # Control buttons
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("📊 Risk vs Return Chart", use_container_width=True):
                st.session_state.show_chart = "risk_return"

        with col2:
            if st.button("🎯 Recommendation Strength", use_container_width=True):
                st.session_state.show_chart = "strength"

        with col3:
            if st.button("💹 Price Target Analysis", use_container_width=True):
                st.session_state.show_chart = "price_target"

        with col4:
            if st.button("🏢 Sector Allocation", use_container_width=True):
                st.session_state.show_chart = "sector"

        if 'show_chart' not in st.session_state:
            st.session_state.show_chart = "risk_return"

        # Display selected chart
        if st.session_state.show_chart == "risk_return":
            st.subheader("📊 Risk vs Return Analysis (Tailored to Your Profile)")

            fig = go.Figure()

            # Color mapping based on recommendation strength and risk alignment
            colors = []
            for i, row in df.iterrows():
                strength = row['strength']
                stock_risk = row['risk']

                # Highlight stocks that match user's risk profile
                risk_match = abs(stock_risk - user_risk_level) <= 2

                if risk_match and strength >= 0.8:
                    colors.append('#00FF41')  # Perfect Match - Bright Green
                elif risk_match and strength >= 0.7:
                    colors.append('#32CD32')  # Good Match - Light Green
                elif strength >= 0.8:
                    colors.append('#FFD700')  # Strong but different risk - Gold
                elif strength >= 0.7:
                    colors.append('#FFA500')  # Good but different risk - Orange
                else:
                    colors.append('#FF1744')  # Poor match - Red

            # Create size array based on market cap
            sizes = (df['market_cap'] / 50).tolist()

            fig.add_trace(go.Scatter(
                x=df['risk'],
                y=df['upside'],
                mode='markers+text',
                marker=dict(
                    size=sizes,
                    color=colors,
                    opacity=0.8,
                    line=dict(width=2, color='#FFFFFF')
                ),
                text=df['symbol'],
                textposition="middle center",
                customdata=df[['company', 'sector', 'strength', 'price', 'target']],
                hovertemplate=
                '<b>%{text}</b><br>' +
                'Company: %{customdata[0]}<br>' +
                'Sector: %{customdata[1]}<br>' +
                'Risk Level: %{x}<br>' +
                'Potential Upside: %{y:.1f}%<br>' +
                'AI Strength: %{customdata[2]:.1%}<br>' +
                'Current Price: $%{customdata[3]:.2f}<br>' +
                'Target Price: $%{customdata[4]:.2f}<br>' +
                '<extra></extra>',
                textfont=dict(color='white', size=10, family='Arial Black')
            ))

            fig.update_layout(
                title=dict(
                    text="Risk vs Return Analysis",
                    font=dict(color='#DC143C', size=20),
                    x=0.5
                ),
                xaxis=dict(
                    title="Risk Level (1-10)",
                    color='white',
                    gridcolor='#333'
                ),
                yaxis=dict(
                    title="Potential Upside (%)",
                    color='white',
                    gridcolor='#333'
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=500
            )

            st.plotly_chart(fig, use_container_width=True)

            # Add color legend and explanations
            st.markdown("### 📊 Chart Legend & Risk Alignment")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("""
                **🎨 Color Coding:**
                - 🟢 **Bright Green**: Perfect Risk Match + Strong AI (80%+)
                - 🟢 **Light Green**: Good Risk Match + Good AI (70%+)
                - 🟡 **Gold**: Strong AI but Different Risk Level
                - 🟠 **Orange**: Good AI but Different Risk Level
                - 🔴 **Red**: Poor AI Match or High Risk Mismatch
                """)

            with col2:
                # Calculate and display risk alignment stats
                perfect_matches = len([c for c in colors if c == '#00FF41'])
                good_matches = len([c for c in colors if c == '#32CD32'])
                total_recommendations = len(colors)

                st.markdown(f"""
                **📈 Your Risk Alignment:**
                - 🎯 Perfect Matches: **{perfect_matches}** stocks
                - ✅ Good Matches: **{good_matches}** stocks
                - 📊 Total Analyzed: **{total_recommendations}** stocks
                - 🔥 Alignment Score: **{((perfect_matches + good_matches) / total_recommendations * 100):.1f}%**
                """)

            # Add risk zone indicator
            st.markdown("---")
            risk_zone_color = '#00FF41' if user_risk_level <= 3 else '#FFD700' if user_risk_level <= 6 else '#FF1744'
            risk_zone_text = 'Conservative' if user_risk_level <= 3 else 'Moderate' if user_risk_level <= 6 else 'Aggressive'

            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                        padding: 15px; border-radius: 10px; border: 2px solid {risk_zone_color};
                        text-align: center; margin: 10px 0;'>
                <h4 style='color: {risk_zone_color}; margin: 0;'>
                    🎯 You are in the <strong>{risk_zone_text}</strong> Risk Zone (Level {user_risk_level})
                </h4>
                <p style='color: #ccc; margin: 5px 0 0 0;'>
                    Stocks highlighted in green are perfectly aligned with your risk profile
                </p>
            </div>
            """, unsafe_allow_html=True)

        elif st.session_state.show_chart == "strength":
            st.subheader("🎯 Recommendation Strength Analysis")

            # Sort by strength for better visualization
            df_sorted = df.sort_values('strength', ascending=True)

            fig = go.Figure()

            # Enhanced color coding based on both strength and risk alignment
            colors = []
            for i, row in df_sorted.iterrows():
                strength = row['strength']
                stock_risk = row['risk']

                # Check risk alignment with user profile
                risk_match = abs(stock_risk - user_risk_level) <= 2

                if risk_match and strength >= 0.8:
                    colors.append('#00FF41')  # Perfect match
                elif risk_match and strength >= 0.7:
                    colors.append('#32CD32')  # Good match
                elif strength >= 0.8:
                    colors.append('#FFD700')  # Strong but misaligned risk
                elif strength >= 0.7:
                    colors.append('#FFA500')  # Good but misaligned risk
                elif strength >= 0.6:
                    colors.append('#FF8C00')  # Moderate
                else:
                    colors.append('#FF1744')  # Poor match

            fig.add_trace(go.Bar(
                y=df_sorted['symbol'],
                x=df_sorted['strength'] * 100,
                orientation='h',
                marker=dict(
                    color=colors,
                    line=dict(color='#DC143C', width=1)
                ),
                text=[f"{x:.0%}" for x in df_sorted['strength']],
                textposition='inside',
                textfont=dict(color='white', size=12),
                customdata=df_sorted[['company', 'sector', 'risk', 'upside', 'price', 'target']],
                hovertemplate=
                '<b>%{y}</b><br>' +
                'Company: %{customdata[0]}<br>' +
                'Sector: %{customdata[1]}<br>' +
                'AI Strength: %{x:.1f}%<br>' +
                'Risk Level: %{customdata[2]}<br>' +
                'Potential Upside: %{customdata[3]:.1f}%<br>' +
                'Price: $%{customdata[4]:.2f} → $%{customdata[5]:.2f}<br>' +
                '<extra></extra>'
            ))

            fig.update_layout(
                title=dict(
                    text="AI Recommendation Strength",
                    font=dict(color='#DC143C', size=20),
                    x=0.5
                ),
                xaxis=dict(
                    title="Recommendation Strength (%)",
                    color='white',
                    gridcolor='#333',
                    range=[0, 100]
                ),
                yaxis=dict(
                    title="Stock Symbol",
                    color='white'
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=500
            )

            st.plotly_chart(fig, use_container_width=True)

        elif st.session_state.show_chart == "price_target":
            st.subheader("💹 Price Target Analysis")

            fig = go.Figure()

            # Create risk-aligned colors for current and target prices
            current_colors = []
            target_colors = []

            for i, row in df.iterrows():
                stock_risk = row['risk']
                strength = row['strength']
                risk_match = abs(stock_risk - user_risk_level) <= 2

                if risk_match and strength >= 0.8:
                    current_colors.append('#8B0000')  # Dark red for perfect match
                    target_colors.append('#00FF41')  # Bright green for perfect match
                elif risk_match and strength >= 0.7:
                    target_colors.append('#32CD32')  # Light green for good match
                    current_colors.append('#DC143C')  # Standard red
                else:
                    current_colors.append('#FF6B6B')  # Light red for mismatches
                    target_colors.append('#90EE90')  # Light green for mismatches

            # Current prices
            fig.add_trace(go.Bar(
                name='Current Price',
                x=df['symbol'],
                y=df['price'],
                marker=dict(color=current_colors, opacity=0.8),
                customdata=df[['company', 'sector', 'strength', 'risk', 'upside']],
                hovertemplate=
                '<b>%{x} - Current Price</b><br>' +
                'Company: %{customdata[0]}<br>' +
                'Sector: %{customdata[1]}<br>' +
                'Current Price: $%{y:.2f}<br>' +
                'AI Strength: %{customdata[2]:.1%}<br>' +
                'Risk Level: %{customdata[3]}<br>' +
                '<extra></extra>'
            ))

            # Target prices
            fig.add_trace(go.Bar(
                name='Target Price',
                x=df['symbol'],
                y=df['target'],
                marker=dict(color=target_colors, opacity=0.8),
                customdata=df[['company', 'sector', 'strength', 'risk', 'upside']],
                hovertemplate=
                '<b>%{x} - Target Price</b><br>' +
                'Company: %{customdata[0]}<br>' +
                'Sector: %{customdata[1]}<br>' +
                'Target Price: $%{y:.2f}<br>' +
                'Potential Upside: %{customdata[4]:.1f}%<br>' +
                'AI Strength: %{customdata[2]:.1%}<br>' +
                'Risk Level: %{customdata[3]}<br>' +
                '<extra></extra>'
            ))

            fig.update_layout(
                title=dict(
                    text="Current vs Target Price Analysis",
                    font=dict(color='#DC143C', size=20),
                    x=0.5
                ),
                xaxis=dict(
                    title="Stock Symbol",
                    color='white'
                ),
                yaxis=dict(
                    title="Price ($)",
                    color='white',
                    gridcolor='#333'
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                barmode='group',
                height=500,
                legend=dict(
                    font=dict(color='white')
                )
            )

            st.plotly_chart(fig, use_container_width=True)

        elif st.session_state.show_chart == "sector":
            st.subheader("🏢 Sector Allocation Analysis")

            sector_data = df.groupby('sector').agg({
                'strength': 'mean',
                'upside': 'mean',
                'symbol': 'count'
            }).reset_index()
            sector_data.columns = ['sector', 'avg_strength', 'avg_upside', 'count']

            fig = go.Figure(data=[go.Pie(
                labels=sector_data['sector'],
                values=sector_data['count'],
                hole=0.4,
                marker=dict(
                    colors=['#DC143C', '#00FF41', '#FFD700', '#FF6B6B', '#4ECDC4'],
                    line=dict(color='#000000', width=2)
                ),
                textfont=dict(color='white', size=12)
            )])

            fig.update_layout(
                title=dict(
                    text="Recommended Stocks by Sector",
                    font=dict(color='#DC143C', size=20),
                    x=0.5
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=500
            )

            st.plotly_chart(fig, use_container_width=True)

        # AI-Powered Summary Section
        st.markdown("---")
        st.markdown("### 🤖 AI CHOPRA'S PERSONALIZED INSIGHTS")

        # Calculate key metrics for summary
        perfect_matches = len([1 for i, row in df.iterrows()
                             if abs(row['risk'] - user_risk_level) <= 2 and row['strength'] >= 0.8])
        good_matches = len([1 for i, row in df.iterrows()
                          if abs(row['risk'] - user_risk_level) <= 2 and row['strength'] >= 0.7])
        total_stocks = len(df)
        avg_upside = df['upside'].mean()
        best_stock = df.loc[df['strength'].idxmax()]
        top_sector = df['sector'].mode()[0] if not df.empty else "Technology"

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #0d1b2a 0%, #1b263b 100%);
                        padding: 20px; border-radius: 15px; border: 2px solid #00FF41;'>
                <h4 style='color: #00FF41; margin: 0; text-align: center;'>🎯 YOUR PERFECT MATCHES</h4>
                <div style='text-align: center; margin: 15px 0;'>
                    <div style='font-size: 2rem; color: #00FF41; font-weight: bold;'>{perfect_matches}</div>
                    <div style='color: #ccc; font-size: 0.9rem;'>Perfect Risk Alignment + Strong AI</div>
                </div>
                <p style='color: #ccc; margin: 10px 0; text-align: center;'>
                    Out of {total_stocks} analyzed stocks, {perfect_matches + good_matches} align with your
                    <strong>Level {user_risk_level}</strong> risk profile
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #2d1b0d 0%, #3b2b1b 100%);
                        padding: 20px; border-radius: 15px; border: 2px solid #FFD700;'>
                <h4 style='color: #FFD700; margin: 0; text-align: center;'>🚀 TOP RECOMMENDATION</h4>
                <div style='text-align: center; margin: 15px 0;'>
                    <div style='font-size: 1.5rem; color: #FFD700; font-weight: bold;'>{best_stock['symbol']}</div>
                    <div style='color: #ccc; font-size: 0.9rem;'>{best_stock['company']}</div>
                </div>
                <p style='color: #ccc; margin: 10px 0; text-align: center;'>
                    <strong>{best_stock['strength']:.1%}</strong> AI Confidence<br>
                    <strong>{best_stock['upside']:.1f}%</strong> Potential Upside<br>
                    Risk Level: <strong>{best_stock['risk']}</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)

        # AI-Generated Market Insights
        st.markdown("### 💡 AI Market Intelligence")

        # Generate personalized insights based on user's risk profile and current recommendations
        if user_risk_level <= 3:
            risk_advice = f"""
            **Conservative Strategy Recommendation:**
            As a conservative investor (Risk Level {user_risk_level}), Agent Chopra recommends focusing on dividend-yielding blue chips.
            Your current selections show an average potential upside of {avg_upside:.1f}%, which aligns well with stable growth expectations.
            Consider sectors like {top_sector} for steady performance.
            """
        elif user_risk_level <= 6:
            risk_advice = f"""
            **Moderate Strategy Recommendation:**
            With your moderate risk profile (Risk Level {user_risk_level}), you have access to a balanced mix of growth and value stocks.
            The current portfolio shows {avg_upside:.1f}% average upside potential. Agent Chopra suggests diversifying across
            {top_sector} and other sectors to optimize risk-adjusted returns.
            """
        else:
            risk_advice = f"""
            **Aggressive Strategy Recommendation:**
            Your aggressive risk profile (Risk Level {user_risk_level}) allows for high-growth opportunities.
            Current recommendations show {avg_upside:.1f}% average upside potential. Agent Chopra identifies strong momentum
            in {top_sector} sector. Consider higher position sizing for your top-conviction plays.
            """

        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #1a1a2e 0%, #2d2d4d 100%);
                    padding: 20px; border-radius: 15px; border: 2px solid #DC143C; margin: 15px 0;'>
            <h4 style='color: #DC143C; margin: 0;'>🧠 AGENT CHOPRA'S ANALYSIS</h4>
            <p style='color: #ccc; margin: 15px 0; line-height: 1.6;'>
                {risk_advice}
            </p>
            <div style='border-top: 1px solid #444; padding-top: 15px; margin-top: 15px;'>
                <strong style='color: #FFD700;'>🔥 Key Insights:</strong>
                <ul style='color: #ccc; margin: 10px 0; padding-left: 20px;'>
                    <li>Market sentiment analysis suggests {"bullish" if avg_upside > 15 else "neutral"} conditions</li>
                    <li>{perfect_matches} stocks perfectly match your risk tolerance</li>
                    <li>Recommended sector focus: <strong>{top_sector}</strong></li>
                    <li>Average potential upside: <strong>{avg_upside:.1f}%</strong></li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Investment interface
        st.markdown("---")
        st.subheader("💰 Quick Investment Actions")

        col1, col2 = st.columns(2)

        with col1:
            selected_stock = st.selectbox(
                "Select Stock to Invest",
                df['symbol'].tolist(),
                format_func=lambda x: f"{x} - {df[df['symbol']==x]['company'].iloc[0]}"
            )

        with col2:
            investment_amount = st.number_input(
                "Investment Amount ($)",
                min_value=10.0,
                max_value=10000.0,
                value=1000.0,
                step=100.0
            )

        if selected_stock:
            stock_data = df[df['symbol'] == selected_stock].iloc[0]
            shares = int(investment_amount / stock_data['price'])
            total_cost = shares * stock_data['price']

            col3, col4, col5 = st.columns(3)

            with col3:
                st.metric("Shares to Buy", f"{shares}")

            with col4:
                st.metric("Total Cost", f"${total_cost:,.2f}")

            with col5:
                st.metric("Potential Gain", f"${(shares * (stock_data['target'] - stock_data['price'])):,.2f}")

            col_buy, col_watchlist = st.columns(2)

            with col_buy:
                if st.button(f"📈 BUY {selected_stock}", type="primary", use_container_width=True):
                    st.success(f"🎉 Order placed for {shares} shares of {selected_stock}!")

            with col_watchlist:
                if st.button(f"👁️ Add to Watchlist", use_container_width=True):
                    # Initialize watchlist in session state
                    if 'user_watchlist' not in st.session_state:
                        st.session_state.user_watchlist = []

                    # Add to watchlist if not already there
                    if selected_stock not in st.session_state.user_watchlist:
                        st.session_state.user_watchlist.append(selected_stock)
                        st.success(f"✅ {selected_stock} added to watchlist!")
                    else:
                        st.warning(f"⚠️ {selected_stock} is already in your watchlist!")

        # Auto-Trading Status Display
        if st.session_state.get('auto_trading_active', False):
            st.markdown("---")
            col1, col2, col3 = st.columns(3)

            with col1:
                daily_trades = st.session_state.get('daily_auto_trades', 0)
                max_trades = st.session_state.get('auto_trading_settings', {}).get('max_daily_trades', 0)
                st.metric("🤖 Auto-Trades Today", f"{daily_trades}/{max_trades}")

            with col2:
                confidence = st.session_state.get('auto_trading_settings', {}).get('confidence_threshold', 0)
                st.metric("🎯 Confidence Threshold", f"{confidence:.1%}")

            with col3:
                max_position = st.session_state.get('auto_trading_settings', {}).get('max_position_size', 0)
                st.metric("📊 Max Position Size", f"{max_position}%")

    def render_about_section(self):
        """Render the About section with project details"""
        st.markdown("""
        <div style='background: linear-gradient(135deg, #1a1a1a 0%, #2d1b1b 100%);
                    padding: 30px; border-radius: 15px; margin-bottom: 20px;
                    border: 2px solid #DC143C;'>
            <div style='text-align: center; margin-bottom: 30px;'>
                <h1 style='color: #DC143C; margin: 0; font-size: 3rem;'>🔥 AGENT CHOPRA</h1>
                <h2 style='color: #888; margin: 10px 0; font-style: italic;'>by NAVADA Trading Intelligence</h2>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Summary Section
        st.markdown("### 📋 Summary")
        st.markdown("""
        **AGENT CHOPRA** is an AI-powered trading assistant built on the NAVADA platform, designed to automate
        paper and live trading through Alpaca's API. It acts as your personal market agent — analyzing trends,
        executing trades, and learning from performance over time. Built for both beginners and developers,
        AGENT CHOPRA helps users experiment, refine, and master algorithmic trading strategies safely before going live.
        """)

        # Core Focus Section
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🎯 Core Focus")
            st.markdown("""
            • **Smart, autonomous trading** via Alpaca's Paper API
            • **Strategy simulation** and performance tracking
            • **Real-time market monitoring** and adaptive execution
            • **Risk-controlled, data-driven** decision logic
            """)

        with col2:
            st.markdown("### 🚀 Vision")
            st.markdown("""
            To transform how individuals learn and interact with financial markets — by blending
            **creativity**, **automation**, and **intelligence** into a single intuitive trading companion.
            """)

        # Features Section
        st.markdown("### ⚡ Key Features")

        feature_col1, feature_col2, feature_col3 = st.columns(3)

        with feature_col1:
            st.markdown("""
            **🤖 AI Assistant**
            - Intelligent stock recommendations
            - Risk-based portfolio guidance
            - Real-time market analysis
            - Natural language queries
            """)

        with feature_col2:
            st.markdown("""
            **📊 Trading Dashboard**
            - Live portfolio tracking
            - P&L analysis
            - Position management
            - Risk profiling system
            """)

        with feature_col3:
            st.markdown("""
            **🔍 Market Intelligence**
            - Alpha Vantage integration
            - Brave Search news feed
            - Technical indicators
            - Market sentiment analysis
            """)

        # Technology Stack
        st.markdown("### 🛠️ Technology Stack")
        tech_col1, tech_col2 = st.columns(2)

        with tech_col1:
            st.markdown("""
            **Backend:**
            - Python 3.11+
            - Streamlit Framework
            - Alpaca Trading API
            - OpenAI GPT-4
            - LangChain RAG
            """)

        with tech_col2:
            st.markdown("""
            **Integrations:**
            - Alpha Vantage API
            - Brave Search API
            - SQLite Database
            - ChromaDB Vector Store
            - Plotly Visualizations
            """)

        # Developer Section
        st.markdown("---")
        st.markdown("### 👨‍💻 Developer")
        dev_col1, dev_col2, dev_col3 = st.columns([1, 2, 1])

        with dev_col2:
            st.markdown("""
            <div style='text-align: center; background: #161B22; padding: 20px; border-radius: 10px; border: 1px solid #DC143C;'>
                <h3 style='color: #DC143C; margin: 0;'>Lee Akpareva MBA, MA</h3>
                <p style='color: #888; margin: 10px 0 0 0;'>Lead Developer & AI Engineer</p>
                <p style='color: #888; margin: 5px 0; font-size: 0.9rem;'>NAVADA Trading Intelligence</p>
            </div>
            """, unsafe_allow_html=True)

        # Disclaimer
        st.markdown("---")
        st.warning("""
        **⚠️ Important Disclaimer:**
        AGENT CHOPRA is designed for educational and paper trading purposes.
        All trading involves risk, and past performance does not guarantee future results.
        Always conduct your own research and consider your financial situation before making investment decisions.
        """)

        # Version Info
        st.markdown("---")
        info_col1, info_col2, info_col3 = st.columns(3)

        with info_col1:
            st.info("**Version:** 2.0.0")

        with info_col2:
            st.info("**Environment:** Paper Trading")

        with info_col3:
            st.info("**Status:** Production Ready")

    def run(self):
        """Main application entry point"""
        self.render_header()

        # Sidebar
        refresh_rate = self.render_sidebar()

        # Main content tabs
        if st.session_state.ai_assistant:
            if ADVANCED_FEATURES_AVAILABLE:
                tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs([
                    "Command Center",
                    "AI Assistant",
                    "AI Insights",
                    "Recommendations",
                    "Daily P&L",
                    "Watchlist",
                    "Market News",
                    "Research",
                    "Voice Assistant",
                    "Visual Analytics",
                    "About"
                ])
            else:
                tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                    "Command Center",
                    "AI Assistant",
                    "AI Insights",
                    "Recommendations",
                    "Risk Profile",
                    "About"
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
                                    <strong>{profile.level.name.replace('_', ' ').title()}</strong>
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
                    self.render_watchlist_management()

                with tab7:  # Market News
                    create_google_news_dashboard(st.session_state.google_news_api)

                with tab8:  # Research
                    create_market_research_dashboard(st.session_state.brave_search_api, st.session_state.market_researcher)

                with tab9:  # Voice Assistant
                    create_voice_interface()

                with tab10:  # Visual Analytics
                    create_visual_analytics_dashboard()

                with tab11:  # About
                    self.render_about_section()

            else:
                # Handle About tab for non-advanced features
                with tab6:  # About
                    self.render_about_section()

        # Footer
        st.markdown("---")

        # Status row
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

        # Developer credits row
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(
                "<div style='text-align: center; color: #888; padding: 10px;'>"
                "<p style='margin: 0;'>🔥 <strong>AGENT CHOPRA</strong> by NAVADA Trading Intelligence</p>"
                "<p style='margin: 5px 0 0 0; font-size: 0.8rem;'>Designed and Developed by <strong>Lee Akpareva MBA, MA</strong></p>"
                "</div>",
                unsafe_allow_html=True
            )

def main():
    """Entry point"""
    app = AgentChopra()
    app.run()

if __name__ == "__main__":
    main()