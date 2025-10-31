#!/usr/bin/env python3
"""
Brave Search Integration for Agent Chopra
Real-time web search capabilities for market research and news
"""

import requests
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class BraveSearchAPI:
    """Brave Search API integration for real-time market research"""

    def __init__(self):
        self.api_key = os.getenv('BRAVE_SEARCH_API_KEY')
        self.base_url = "https://api.search.brave.com/res/v1"
        self.headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip'
        }

        if self.api_key:
            self.headers['X-Subscription-Token'] = self.api_key
        else:
            st.warning("⚠️ Brave Search API key not configured. Search features will be limited.")

    def web_search(self, query: str, count: int = 10, safesearch: str = "moderate") -> Optional[Dict]:
        """Perform web search using Brave Search API"""
        if not self.api_key:
            return None

        params = {
            'q': query,
            'count': count,
            'safesearch': safesearch,
            'text_decorations': False,
            'search_lang': 'en',
            'country': 'US',
            'spellcheck': True
        }

        try:
            response = requests.get(
                f"{self.base_url}/web/search",
                headers=self.headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()

        except Exception as e:
            st.error(f"Brave Search API error: {str(e)}")
            return None

    def news_search(self, query: str, count: int = 10, safesearch: str = "moderate") -> Optional[Dict]:
        """Perform news search using Brave Search API"""
        if not self.api_key:
            return None

        params = {
            'q': query,
            'count': count,
            'safesearch': safesearch,
            'text_decorations': False,
            'search_lang': 'en',
            'country': 'US',
            'freshness': 'pd'  # Past day
        }

        try:
            response = requests.get(
                f"{self.base_url}/news/search",
                headers=self.headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()

        except Exception as e:
            st.error(f"Brave News Search API error: {str(e)}")
            return None

class MarketResearcher:
    """Advanced market research using Brave Search"""

    def __init__(self, brave_api: BraveSearchAPI):
        self.brave_api = brave_api

    def research_company(self, symbol: str) -> Dict:
        """Comprehensive company research"""
        research_data = {
            'symbol': symbol,
            'timestamp': datetime.now(),
            'web_results': [],
            'news_results': [],
            'analysis': {}
        }

        # Web search for company information
        web_query = f"{symbol} stock company profile financial analysis"
        web_results = self.brave_api.web_search(web_query, count=5)

        if web_results and 'web' in web_results:
            research_data['web_results'] = web_results['web']['results']

        # News search for recent developments
        news_query = f"{symbol} stock news earnings financial"
        news_results = self.brave_api.news_search(news_query, count=5)

        if news_results and 'results' in news_results:
            research_data['news_results'] = news_results['results']

        return research_data

    def search_market_trends(self, trend: str) -> Dict:
        """Search for specific market trends and analysis"""
        trend_data = {
            'trend': trend,
            'timestamp': datetime.now(),
            'web_results': [],
            'news_results': []
        }

        # Web search for trend analysis
        web_query = f"{trend} market trend analysis investment opportunity"
        web_results = self.brave_api.web_search(web_query, count=8)

        if web_results and 'web' in web_results:
            trend_data['web_results'] = web_results['web']['results']

        # News search for trend coverage
        news_query = f"{trend} market news investment"
        news_results = self.brave_api.news_search(news_query, count=5)

        if news_results and 'results' in news_results:
            trend_data['news_results'] = news_results['results']

        return trend_data

    def competitor_analysis(self, symbol: str, competitors: List[str]) -> Dict:
        """Analyze company against competitors"""
        analysis = {
            'primary_company': symbol,
            'competitors': competitors,
            'comparison_data': {},
            'timestamp': datetime.now()
        }

        # Research primary company
        primary_query = f"{symbol} vs competitors market share financial performance"
        primary_results = self.brave_api.web_search(primary_query, count=5)

        if primary_results and 'web' in primary_results:
            analysis['comparison_data'][symbol] = primary_results['web']['results']

        # Research each competitor
        for competitor in competitors:
            comp_query = f"{symbol} vs {competitor} comparison financial analysis"
            comp_results = self.brave_api.web_search(comp_query, count=3)

            if comp_results and 'web' in comp_results:
                analysis['comparison_data'][competitor] = comp_results['web']['results']

        return analysis

def create_market_research_dashboard(brave_api: BraveSearchAPI, researcher: MarketResearcher):
    """Create the market research dashboard"""
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1a1a1a 0%, #2d1b1b 100%);
                padding: 20px; border-radius: 10px; margin-bottom: 20px;
                border: 1px solid #DC143C;'>
        <h2 style='color: #DC143C; margin: 0; text-align: center;'>
            🔍 Market Research Center
        </h2>
        <p style='color: #888; text-align: center; margin: 5px 0 0 0;'>
            Real-time market research powered by Brave Search
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Research tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🏢 Company Research", "📈 Trend Analysis", "⚔️ Competitor Analysis", "🔍 Custom Search"])

    with tab1:
        st.markdown("### 🏢 Company Deep Dive")

        col1, col2 = st.columns([3, 1])
        with col1:
            research_symbol = st.text_input("Enter stock symbol for research", placeholder="e.g., AAPL, MSFT, TSLA")
        with col2:
            research_btn = st.button("🔍 Research", type="primary")

        if research_btn and research_symbol:
            with st.spinner(f"Researching {research_symbol.upper()}..."):
                research_data = researcher.research_company(research_symbol.upper())

                # Display web results
                if research_data['web_results']:
                    st.markdown("#### 🌐 Web Analysis")
                    for result in research_data['web_results'][:3]:
                        st.markdown(f"""
                        <div style='background: #1a1a1a; padding: 15px; border-radius: 8px;
                                    margin-bottom: 10px; border-left: 3px solid #DC143C;'>
                            <h4 style='color: #DC143C; margin: 0 0 10px 0;'>
                                <a href="{result.get('url', '#')}" target="_blank" style='color: #DC143C; text-decoration: none;'>
                                    {result.get('title', 'No Title')}
                                </a>
                            </h4>
                            <p style='color: #ccc; margin: 0 0 10px 0;'>{result.get('description', 'No description available')}</p>
                            <small style='color: #888;'>{result.get('url', '')}</small>
                        </div>
                        """, unsafe_allow_html=True)

                # Display news results
                if research_data['news_results']:
                    st.markdown("#### 📰 Recent News")
                    for news in research_data['news_results'][:3]:
                        st.markdown(f"""
                        <div style='background: #1a1a1a; padding: 15px; border-radius: 8px;
                                    margin-bottom: 10px; border-left: 3px solid #00FF41;'>
                            <h4 style='color: #00FF41; margin: 0 0 10px 0;'>
                                <a href="{news.get('url', '#')}" target="_blank" style='color: #00FF41; text-decoration: none;'>
                                    {news.get('title', 'No Title')}
                                </a>
                            </h4>
                            <p style='color: #ccc; margin: 0 0 10px 0;'>{news.get('description', 'No description available')}</p>
                            <div style='display: flex; justify-content: space-between;'>
                                <small style='color: #888;'>{news.get('meta_url', {}).get('hostname', 'Unknown Source')}</small>
                                <small style='color: #888;'>{news.get('age', '')}</small>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("### 📈 Market Trend Analysis")

        trend_options = [
            "AI and Machine Learning stocks",
            "Electric Vehicle market",
            "Renewable Energy investments",
            "Cryptocurrency market trends",
            "Biotech and Healthcare innovations",
            "Cloud Computing growth",
            "5G Technology adoption",
            "Cybersecurity investments"
        ]

        col1, col2 = st.columns([3, 1])
        with col1:
            selected_trend = st.selectbox("Select a trend to analyze", trend_options)
            custom_trend = st.text_input("Or enter custom trend", placeholder="e.g., quantum computing stocks")
        with col2:
            trend_btn = st.button("🔍 Analyze Trend", type="primary")

        if trend_btn:
            trend_to_analyze = custom_trend if custom_trend else selected_trend

            with st.spinner(f"Analyzing trend: {trend_to_analyze}..."):
                trend_data = researcher.search_market_trends(trend_to_analyze)

                # Display trend analysis
                if trend_data['web_results']:
                    st.markdown("#### 📊 Trend Analysis")
                    for result in trend_data['web_results'][:4]:
                        st.markdown(f"""
                        <div style='background: #1a1a1a; padding: 15px; border-radius: 8px;
                                    margin-bottom: 10px; border-left: 3px solid #FFD700;'>
                            <h4 style='color: #FFD700; margin: 0 0 10px 0;'>
                                <a href="{result.get('url', '#')}" target="_blank" style='color: #FFD700; text-decoration: none;'>
                                    {result.get('title', 'No Title')}
                                </a>
                            </h4>
                            <p style='color: #ccc; margin: 0 0 10px 0;'>{result.get('description', 'No description available')}</p>
                            <small style='color: #888;'>{result.get('url', '')}</small>
                        </div>
                        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("### ⚔️ Competitor Analysis")

        col1, col2 = st.columns(2)
        with col1:
            primary_company = st.text_input("Primary company symbol", placeholder="e.g., AAPL")
        with col2:
            competitors_input = st.text_input("Competitor symbols (comma-separated)", placeholder="e.g., MSFT, GOOGL, META")

        if st.button("🔍 Analyze Competition", type="primary") and primary_company and competitors_input:
            competitors = [comp.strip().upper() for comp in competitors_input.split(',')]

            with st.spinner(f"Analyzing {primary_company.upper()} vs competitors..."):
                comp_analysis = researcher.competitor_analysis(primary_company.upper(), competitors)

                # Display competitive analysis
                if comp_analysis['comparison_data']:
                    st.markdown("#### ⚔️ Competitive Landscape")

                    for company, results in comp_analysis['comparison_data'].items():
                        if results:
                            st.markdown(f"**{company} Analysis:**")
                            for result in results[:2]:
                                st.markdown(f"""
                                <div style='background: #1a1a1a; padding: 10px; border-radius: 8px;
                                            margin-bottom: 8px; border-left: 2px solid #DC143C;'>
                                    <h5 style='color: #DC143C; margin: 0 0 5px 0;'>
                                        <a href="{result.get('url', '#')}" target="_blank" style='color: #DC143C; text-decoration: none;'>
                                            {result.get('title', 'No Title')}
                                        </a>
                                    </h5>
                                    <p style='color: #ccc; margin: 0; font-size: 0.9em;'>{result.get('description', 'No description available')[:150]}...</p>
                                </div>
                                """, unsafe_allow_html=True)

    with tab4:
        st.markdown("### 🔍 Custom Market Search")

        search_query = st.text_input("Enter your search query", placeholder="e.g., best dividend stocks 2024, market crash prediction")

        col1, col2 = st.columns(2)
        with col1:
            search_type = st.selectbox("Search type", ["Web Search", "News Search"])
        with col2:
            result_count = st.slider("Number of results", 3, 15, 8)

        if st.button("🔍 Search", type="primary") and search_query:
            with st.spinner(f"Searching for: {search_query}..."):
                if search_type == "Web Search":
                    results = brave_api.web_search(search_query, count=result_count)
                    results_key = 'web'
                    results_list = results.get('web', {}).get('results', []) if results else []
                else:
                    results = brave_api.news_search(search_query, count=result_count)
                    results_list = results.get('results', []) if results else []

                if results_list:
                    st.markdown(f"#### 🔍 Search Results for '{search_query}'")

                    for result in results_list:
                        if search_type == "Web Search":
                            st.markdown(f"""
                            <div style='background: #1a1a1a; padding: 15px; border-radius: 8px;
                                        margin-bottom: 10px; border-left: 3px solid #DC143C;'>
                                <h4 style='color: #DC143C; margin: 0 0 10px 0;'>
                                    <a href="{result.get('url', '#')}" target="_blank" style='color: #DC143C; text-decoration: none;'>
                                        {result.get('title', 'No Title')}
                                    </a>
                                </h4>
                                <p style='color: #ccc; margin: 0 0 10px 0;'>{result.get('description', 'No description available')}</p>
                                <small style='color: #888;'>{result.get('url', '')}</small>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style='background: #1a1a1a; padding: 15px; border-radius: 8px;
                                        margin-bottom: 10px; border-left: 3px solid #00FF41;'>
                                <h4 style='color: #00FF41; margin: 0 0 10px 0;'>
                                    <a href="{result.get('url', '#')}" target="_blank" style='color: #00FF41; text-decoration: none;'>
                                        {result.get('title', 'No Title')}
                                    </a>
                                </h4>
                                <p style='color: #ccc; margin: 0 0 10px 0;'>{result.get('description', 'No description available')}</p>
                                <div style='display: flex; justify-content: space-between;'>
                                    <small style='color: #888;'>{result.get('meta_url', {}).get('hostname', 'Unknown Source')}</small>
                                    <small style='color: #888;'>{result.get('age', '')}</small>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.warning("No results found. Please try a different search query.")

def create_quick_search_widget(brave_api: BraveSearchAPI):
    """Create a quick search widget for the sidebar"""
    st.sidebar.markdown("""
    <div style='background: linear-gradient(135deg, #1a1a1a 0%, #2d1b1b 100%);
                padding: 15px; border-radius: 10px; margin-bottom: 20px;
                border: 1px solid #DC143C;'>
        <h3 style='color: #DC143C; margin: 0; text-align: center;'>🔍 Quick Search</h3>
    </div>
    """, unsafe_allow_html=True)

    quick_query = st.sidebar.text_input("🔍 Quick market search", placeholder="e.g., NVDA earnings")

    if st.sidebar.button("Search", type="primary") and quick_query:
        results = brave_api.web_search(quick_query, count=3)

        if results and 'web' in results:
            st.sidebar.markdown("**Search Results:**")
            for result in results['web']['results'][:2]:
                st.sidebar.markdown(f"""
                <div style='background: #1a1a1a; padding: 10px; border-radius: 5px; margin-bottom: 8px;'>
                    <a href="{result.get('url', '#')}" target="_blank" style='color: #DC143C; text-decoration: none; font-size: 0.9em;'>
                        {result.get('title', 'No Title')[:50]}...
                    </a>
                    <p style='color: #888; margin: 5px 0 0 0; font-size: 0.8em;'>{result.get('description', '')[:80]}...</p>
                </div>
                """, unsafe_allow_html=True)