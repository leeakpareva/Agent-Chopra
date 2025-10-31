#!/usr/bin/env python3
"""
Alpha Vantage Integration for Agent Chopra
Enhanced market data, news, alpha intelligence, and technical analysis features
"""

import requests
import pandas as pd
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import streamlit as st
from dotenv import load_dotenv
import time
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

load_dotenv()

class AlphaVantageAPI:
    """Alpha Vantage API integration for enhanced market data and intelligence"""

    def __init__(self):
        self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.base_url = "https://www.alphavantage.co/query"
        self.cache = {}
        self.cache_expiry = {}

        if not self.api_key:
            st.warning("⚠️ Alpha Vantage API key not configured. Some features may be limited.")

    def _make_request(self, params: Dict) -> Optional[Dict]:
        """Make API request with caching and rate limiting"""
        if not self.api_key:
            return None

        params['apikey'] = self.api_key
        cache_key = str(sorted(params.items()))

        # Check cache first (5 minute expiry)
        if cache_key in self.cache:
            if datetime.now() < self.cache_expiry.get(cache_key, datetime.min):
                return self.cache[cache_key]

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Check for API errors
            if "Error Message" in data:
                st.error(f"Alpha Vantage Error: {data['Error Message']}")
                return None

            if "Note" in data:
                st.warning("Alpha Vantage: API call frequency limit reached. Please try again later.")
                return None

            # Cache successful response
            self.cache[cache_key] = data
            self.cache_expiry[cache_key] = datetime.now() + timedelta(minutes=5)

            return data

        except Exception as e:
            st.error(f"Alpha Vantage API error: {str(e)}")
            return None

    def get_daily_prices(self, symbol: str, outputsize: str = "compact") -> Optional[pd.DataFrame]:
        """Get daily price data for a symbol"""
        params = {
            'function': 'TIME_SERIES_DAILY_ADJUSTED',
            'symbol': symbol,
            'outputsize': outputsize
        }

        data = self._make_request(params)
        if not data or 'Time Series (Daily)' not in data:
            return None

        df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
        df.index = pd.to_datetime(df.index)
        df = df.astype(float)
        df.columns = ['Open', 'High', 'Low', 'Close', 'Adjusted_Close', 'Volume', 'Dividend', 'Split']
        df = df.sort_index(ascending=False)

        return df

    def get_intraday_prices(self, symbol: str, interval: str = "5min") -> Optional[pd.DataFrame]:
        """Get intraday price data"""
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': symbol,
            'interval': interval,
            'outputsize': 'compact'
        }

        data = self._make_request(params)
        if not data or f'Time Series ({interval})' not in data:
            return None

        df = pd.DataFrame.from_dict(data[f'Time Series ({interval})'], orient='index')
        df.index = pd.to_datetime(df.index)
        df = df.astype(float)
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        df = df.sort_index(ascending=False)

        return df

    def get_company_overview(self, symbol: str) -> Optional[Dict]:
        """Get comprehensive company information"""
        params = {
            'function': 'OVERVIEW',
            'symbol': symbol
        }

        data = self._make_request(params)
        if not data or not data.get('Symbol'):
            return None

        return data

    def get_earnings(self, symbol: str) -> Optional[Dict]:
        """Get earnings data for a company"""
        params = {
            'function': 'EARNINGS',
            'symbol': symbol
        }

        return self._make_request(params)

    def get_financial_news(self, tickers: Optional[str] = None, limit: int = 10) -> Optional[List[Dict]]:
        """Get latest financial news"""
        params = {
            'function': 'NEWS_SENTIMENT'
        }

        if tickers:
            params['tickers'] = tickers

        data = self._make_request(params)
        if not data or 'feed' not in data:
            return None

        return data['feed'][:limit]

    def get_top_gainers_losers(self) -> Optional[Dict]:
        """Get top gainers and losers"""
        params = {
            'function': 'TOP_GAINERS_LOSERS'
        }

        return self._make_request(params)

    def get_technical_indicators(self, symbol: str, indicator: str, interval: str = "daily",
                               period: int = 14) -> Optional[pd.DataFrame]:
        """Get technical indicators"""
        params = {
            'function': indicator,
            'symbol': symbol,
            'interval': interval,
            'time_period': period,
            'series_type': 'close'
        }

        data = self._make_request(params)
        if not data:
            return None

        # Find the technical analysis data key
        ta_key = None
        for key in data.keys():
            if 'Technical Analysis' in key:
                ta_key = key
                break

        if not ta_key:
            return None

        df = pd.DataFrame.from_dict(data[ta_key], orient='index')
        df.index = pd.to_datetime(df.index)
        df = df.astype(float)
        df = df.sort_index(ascending=False)

        return df

    def get_economic_indicators(self) -> Dict:
        """Get key economic indicators"""
        indicators = {}

        # Federal Funds Rate
        params = {
            'function': 'FEDERAL_FUNDS_RATE',
            'interval': 'monthly'
        }
        fed_rate = self._make_request(params)
        if fed_rate and 'data' in fed_rate:
            latest_rate = fed_rate['data'][0] if fed_rate['data'] else {}
            indicators['federal_funds_rate'] = latest_rate.get('value', 'N/A')

        # Unemployment Rate
        params = {
            'function': 'UNEMPLOYMENT',
        }
        unemployment = self._make_request(params)
        if unemployment and 'data' in unemployment:
            latest_unemployment = unemployment['data'][0] if unemployment['data'] else {}
            indicators['unemployment_rate'] = latest_unemployment.get('value', 'N/A')

        return indicators

    def get_sector_performance(self) -> Optional[Dict]:
        """Get sector performance data"""
        params = {
            'function': 'SECTOR'
        }
        return self._make_request(params)

    def get_crypto_prices(self, symbol: str = 'BTC', market: str = 'USD') -> Optional[Dict]:
        """Get cryptocurrency prices"""
        params = {
            'function': 'DIGITAL_CURRENCY_DAILY',
            'symbol': symbol,
            'market': market
        }
        return self._make_request(params)

    def create_advanced_chart(self, symbol: str, period: str = '1month') -> Optional[go.Figure]:
        """Create advanced price chart with technical indicators"""
        try:
            # Get price data
            if period == '1day':
                df = self.get_intraday_prices(symbol, '5min')
                title_suffix = "(Intraday 5min)"
            else:
                df = self.get_daily_prices(symbol)
                title_suffix = "(Daily)"

            if df is None or df.empty:
                return None

            # Create candlestick chart with volume
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.05,
                subplot_titles=(f'{symbol} Price {title_suffix}', 'Volume'),
                row_heights=[0.7, 0.3]
            )

            # Price candlestick chart
            fig.add_trace(
                go.Candlestick(
                    x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    name=symbol,
                    increasing_line_color='#00FF41',
                    decreasing_line_color='#FF1744'
                ),
                row=1, col=1
            )

            # Volume bars
            colors = ['#00FF41' if df.iloc[i]['Close'] >= df.iloc[i]['Open']
                     else '#FF1744' for i in range(len(df))]

            fig.add_trace(
                go.Bar(
                    x=df.index,
                    y=df['Volume'],
                    name='Volume',
                    marker_color=colors,
                    opacity=0.7
                ),
                row=2, col=1
            )

            # Update layout
            fig.update_layout(
                title=f'{symbol} Advanced Technical Chart',
                xaxis_rangeslider_visible=False,
                height=600,
                showlegend=True,
                template='plotly_dark',
                font=dict(color='white')
            )

            # Update axes
            fig.update_yaxes(title_text="Price ($)", row=1, col=1)
            fig.update_yaxes(title_text="Volume", row=2, col=1)

            return fig

        except Exception as e:
            st.error(f"Error creating advanced chart: {str(e)}")
            return None

class MarketIntelligence:
    """Advanced market intelligence and analytics"""

    def __init__(self, alpha_api: AlphaVantageAPI):
        self.alpha_api = alpha_api

    def calculate_daily_pnl(self, positions: List[Dict]) -> Dict:
        """Calculate daily P&L for all positions"""
        total_pnl = 0
        position_pnl = []

        for position in positions:
            symbol = position.get('symbol')
            quantity = float(position.get('qty', 0))
            avg_cost = float(position.get('avg_entry_price', 0))

            # Get current price
            current_data = self.alpha_api.get_intraday_prices(symbol)
            if current_data is not None and not current_data.empty:
                current_price = current_data.iloc[0]['Close']

                # Calculate P&L
                position_value = current_price * quantity
                cost_basis = avg_cost * quantity
                pnl = position_value - cost_basis
                pnl_percent = (pnl / cost_basis) * 100 if cost_basis > 0 else 0

                position_pnl.append({
                    'symbol': symbol,
                    'quantity': quantity,
                    'avg_cost': avg_cost,
                    'current_price': current_price,
                    'position_value': position_value,
                    'cost_basis': cost_basis,
                    'pnl': pnl,
                    'pnl_percent': pnl_percent
                })

                total_pnl += pnl

        return {
            'total_pnl': total_pnl,
            'positions': position_pnl,
            'timestamp': datetime.now()
        }

    def get_stock_recommendations(self, risk_level: int) -> List[Dict]:
        """Get stock recommendations based on risk level"""
        # Get top gainers/losers for analysis
        market_data = self.alpha_api.get_top_gainers_losers()

        if not market_data:
            return self._get_default_recommendations(risk_level)

        recommendations = []

        # Risk-based stock selection
        if risk_level <= 3:  # Conservative
            # Focus on stable, dividend-paying stocks
            conservative_picks = [
                {'symbol': 'MSFT', 'reason': 'Stable tech giant with consistent growth', 'risk_score': 2},
                {'symbol': 'JNJ', 'reason': 'Healthcare leader with strong dividends', 'risk_score': 1},
                {'symbol': 'PG', 'reason': 'Consumer staples with recession resistance', 'risk_score': 2},
                {'symbol': 'KO', 'reason': 'Dividend aristocrat with global presence', 'risk_score': 1},
                {'symbol': 'VZ', 'reason': 'Telecom utility with high yield', 'risk_score': 2}
            ]
            recommendations.extend(conservative_picks)

        elif risk_level <= 6:  # Moderate
            # Balanced growth and value
            moderate_picks = [
                {'symbol': 'AAPL', 'reason': 'Tech leader with innovation pipeline', 'risk_score': 4},
                {'symbol': 'GOOGL', 'reason': 'Search dominance with AI advancement', 'risk_score': 5},
                {'symbol': 'UNH', 'reason': 'Healthcare growth with demographic trends', 'risk_score': 3},
                {'symbol': 'HD', 'reason': 'Home improvement with housing market', 'risk_score': 4},
                {'symbol': 'V', 'reason': 'Payment processing with digital growth', 'risk_score': 3}
            ]
            recommendations.extend(moderate_picks)

        else:  # Aggressive (7-10)
            # High growth potential with higher risk
            aggressive_picks = [
                {'symbol': 'TSLA', 'reason': 'EV leader with energy storage growth', 'risk_score': 9},
                {'symbol': 'NVDA', 'reason': 'AI chip dominance with data center boom', 'risk_score': 8},
                {'symbol': 'AMZN', 'reason': 'Cloud and e-commerce expansion', 'risk_score': 7},
                {'symbol': 'META', 'reason': 'Metaverse and social media innovation', 'risk_score': 8},
                {'symbol': 'AMD', 'reason': 'Semiconductor growth with AI demand', 'risk_score': 9}
            ]
            recommendations.extend(aggressive_picks)

        # Add market-based recommendations from gainers/losers
        if 'top_gainers' in market_data:
            for gainer in market_data['top_gainers'][:3]:
                if float(gainer['change_percentage'].replace('%', '')) > 5:
                    recommendations.append({
                        'symbol': gainer['ticker'],
                        'reason': f"Top gainer: +{gainer['change_percentage']} momentum",
                        'risk_score': min(risk_level + 2, 10)
                    })

        return recommendations[:8]  # Limit to 8 recommendations

    def _get_default_recommendations(self, risk_level: int) -> List[Dict]:
        """Fallback recommendations when API is unavailable"""
        all_stocks = {
            1: [('MSFT', 'Microsoft - Stable tech leader'), ('JNJ', 'Johnson & Johnson - Healthcare stability')],
            2: [('PG', 'Procter & Gamble - Consumer staples'), ('KO', 'Coca-Cola - Dividend aristocrat')],
            3: [('AAPL', 'Apple - Innovation with stability'), ('UNH', 'UnitedHealth - Healthcare growth')],
            4: [('GOOGL', 'Alphabet - Search and AI leader'), ('V', 'Visa - Payment processing')],
            5: [('AMZN', 'Amazon - Cloud and commerce'), ('HD', 'Home Depot - Housing market')],
            6: [('META', 'Meta - Social media innovation'), ('NFLX', 'Netflix - Streaming leader')],
            7: [('TSLA', 'Tesla - EV and energy'), ('NVDA', 'NVIDIA - AI chip leader')],
            8: [('AMD', 'AMD - Semiconductor growth'), ('CRM', 'Salesforce - Cloud software')],
            9: [('PLTR', 'Palantir - Big data analytics'), ('SNOW', 'Snowflake - Cloud data')],
            10: [('ARKK', 'ARK Innovation ETF'), ('QQQ', 'NASDAQ ETF - Tech exposure')]
        }

        recommendations = []
        for level in range(1, min(risk_level + 3, 11)):
            if level in all_stocks:
                for symbol, reason in all_stocks[level]:
                    recommendations.append({
                        'symbol': symbol,
                        'reason': reason,
                        'risk_score': level
                    })

        return recommendations[:8]

    def analyze_portfolio_performance(self, positions: List[Dict]) -> Dict:
        """Comprehensive portfolio performance analysis"""
        if not positions:
            return {'error': 'No positions to analyze'}

        analysis = {
            'total_positions': len(positions),
            'sectors': {},
            'risk_distribution': {},
            'performance_metrics': {}
        }

        total_value = 0
        total_cost = 0
        winning_positions = 0

        for position in positions:
            symbol = position.get('symbol')
            quantity = float(position.get('qty', 0))
            avg_cost = float(position.get('avg_entry_price', 0))

            # Get company info for sector analysis
            company_info = self.alpha_api.get_company_overview(symbol)
            if company_info:
                sector = company_info.get('Sector', 'Unknown')
                analysis['sectors'][sector] = analysis['sectors'].get(sector, 0) + 1

            # Calculate values
            current_data = self.alpha_api.get_intraday_prices(symbol)
            if current_data is not None and not current_data.empty:
                current_price = current_data.iloc[0]['Close']
                position_value = current_price * quantity
                cost_basis = avg_cost * quantity

                total_value += position_value
                total_cost += cost_basis

                if current_price > avg_cost:
                    winning_positions += 1

        # Calculate metrics
        if total_cost > 0:
            total_return = ((total_value - total_cost) / total_cost) * 100
            win_rate = (winning_positions / len(positions)) * 100

            analysis['performance_metrics'] = {
                'total_value': total_value,
                'total_cost': total_cost,
                'total_return': total_return,
                'win_rate': win_rate,
                'winning_positions': winning_positions,
                'losing_positions': len(positions) - winning_positions
            }

        return analysis

def create_daily_pnl_dashboard(alpha_api: AlphaVantageAPI, market_intel: MarketIntelligence):
    """Create the daily P&L tracking dashboard"""
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1a1a1a 0%, #2d1b1b 100%);
                padding: 20px; border-radius: 10px; margin-bottom: 20px;
                border: 1px solid #DC143C;'>
        <h2 style='color: #DC143C; margin: 0; text-align: center;'>
            💰 Daily P&L Tracker
        </h2>
        <p style='color: #888; text-align: center; margin: 5px 0 0 0;'>
            Real-time profit & loss tracking powered by Alpha Vantage
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Mock positions for demo (replace with actual portfolio data)
    sample_positions = [
        {'symbol': 'AAPL', 'qty': '10', 'avg_entry_price': '150.00'},
        {'symbol': 'MSFT', 'qty': '5', 'avg_entry_price': '300.00'},
        {'symbol': 'GOOGL', 'qty': '3', 'avg_entry_price': '2500.00'},
    ]

    if st.button("🔄 Calculate Daily P&L", type="primary"):
        with st.spinner("Calculating P&L from Alpha Vantage data..."):
            pnl_data = market_intel.calculate_daily_pnl(sample_positions)

            if pnl_data['positions']:
                total_pnl = pnl_data['total_pnl']

                # Display total P&L
                col1, col2, col3 = st.columns(3)

                with col1:
                    pnl_color = "#00FF41" if total_pnl >= 0 else "#FF1744"
                    st.markdown(f"""
                    <div style='background: #1a1a1a; padding: 15px; border-radius: 8px; text-align: center;'>
                        <h3 style='color: #DC143C; margin: 0;'>Total P&L</h3>
                        <h2 style='color: {pnl_color}; margin: 5px 0;'>${total_pnl:,.2f}</h2>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    winning_positions = sum(1 for pos in pnl_data['positions'] if pos['pnl'] > 0)
                    st.markdown(f"""
                    <div style='background: #1a1a1a; padding: 15px; border-radius: 8px; text-align: center;'>
                        <h3 style='color: #DC143C; margin: 0;'>Winners</h3>
                        <h2 style='color: #00FF41; margin: 5px 0;'>{winning_positions}</h2>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    losing_positions = sum(1 for pos in pnl_data['positions'] if pos['pnl'] < 0)
                    st.markdown(f"""
                    <div style='background: #1a1a1a; padding: 15px; border-radius: 8px; text-align: center;'>
                        <h3 style='color: #DC143C; margin: 0;'>Losers</h3>
                        <h2 style='color: #FF1744; margin: 5px 0;'>{losing_positions}</h2>
                    </div>
                    """, unsafe_allow_html=True)

                # Position details
                st.markdown("### 📊 Position Breakdown")

                pnl_df = pd.DataFrame(pnl_data['positions'])
                st.dataframe(
                    pnl_df.style.format({
                        'avg_cost': '${:.2f}',
                        'current_price': '${:.2f}',
                        'position_value': '${:,.2f}',
                        'cost_basis': '${:,.2f}',
                        'pnl': '${:,.2f}',
                        'pnl_percent': '{:.2f}%'
                    }).applymap(
                        lambda x: 'color: #00FF41' if isinstance(x, (int, float)) and x > 0
                        else 'color: #FF1744' if isinstance(x, (int, float)) and x < 0
                        else '',
                        subset=['pnl', 'pnl_percent']
                    ),
                    use_container_width=True
                )
            else:
                st.warning("Unable to calculate P&L. Please check your Alpha Vantage API key and try again.")

def create_stock_watchlist(alpha_api: AlphaVantageAPI, market_intel: MarketIntelligence):
    """Create stock recommendation watchlist"""
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1a1a1a 0%, #2d1b1b 100%);
                padding: 20px; border-radius: 10px; margin-bottom: 20px;
                border: 1px solid #DC143C;'>
        <h2 style='color: #DC143C; margin: 0; text-align: center;'>
            📈 Smart Stock Watchlist
        </h2>
        <p style='color: #888; text-align: center; margin: 5px 0 0 0;'>
            AI-powered recommendations based on your risk profile
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Risk level selector
    risk_level = st.slider("🎯 Your Risk Level", 1, 10, 5,
                          help="1 = Very Conservative, 10 = Extremely Aggressive")

    if st.button("🔍 Get Recommendations", type="primary"):
        with st.spinner("Analyzing market data for recommendations..."):
            recommendations = market_intel.get_stock_recommendations(risk_level)

            if recommendations:
                st.markdown("### 🎯 Recommended Stocks")

                for i, rec in enumerate(recommendations, 1):
                    col1, col2, col3 = st.columns([1, 3, 1])

                    with col1:
                        st.markdown(f"""
                        <div style='background: #DC143C; padding: 10px; border-radius: 50%;
                                    text-align: center; width: 50px; height: 50px; line-height: 30px;'>
                            <strong style='color: white;'>{rec['symbol']}</strong>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        st.markdown(f"""
                        <div style='padding: 10px;'>
                            <h4 style='color: #DC143C; margin: 0;'>{rec['symbol']}</h4>
                            <p style='color: #ccc; margin: 5px 0;'>{rec['reason']}</p>
                            <small style='color: #888;'>Risk Score: {rec['risk_score']}/10</small>
                        </div>
                        """, unsafe_allow_html=True)

                    with col3:
                        if st.button(f"📊 Analyze", key=f"analyze_{rec['symbol']}"):
                            # Get detailed analysis
                            company_info = alpha_api.get_company_overview(rec['symbol'])
                            if company_info:
                                st.json(company_info)
            else:
                st.warning("Unable to fetch recommendations. Please check your Alpha Vantage API key.")

def create_market_news_section(alpha_api: AlphaVantageAPI):
    """Create daily market news section"""
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1a1a1a 0%, #2d1b1b 100%);
                padding: 20px; border-radius: 10px; margin-bottom: 20px;
                border: 1px solid #DC143C;'>
        <h2 style='color: #DC143C; margin: 0; text-align: center;'>
            📰 Daily Market News
        </h2>
        <p style='color: #888; text-align: center; margin: 5px 0 0 0;'>
            Latest financial news powered by Alpha Vantage
        </p>
    </div>
    """, unsafe_allow_html=True)

    # News categories
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📈 General Market News", type="primary"):
            with st.spinner("Fetching latest market news..."):
                news = alpha_api.get_financial_news(limit=5)

                if news:
                    for article in news:
                        st.markdown(f"""
                        <div style='background: #1a1a1a; padding: 15px; border-radius: 8px;
                                    margin-bottom: 10px; border-left: 3px solid #DC143C;'>
                            <h4 style='color: #DC143C; margin: 0 0 10px 0;'>{article.get('title', 'No Title')}</h4>
                            <p style='color: #ccc; margin: 0 0 10px 0;'>{article.get('summary', 'No summary available')[:200]}...</p>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <small style='color: #888;'>Source: {article.get('source', 'Unknown')}</small>
                                <small style='color: #888;'>{article.get('time_published', '')}</small>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("Unable to fetch news. Please check your Alpha Vantage API key.")

    with col2:
        ticker_input = st.text_input("🔍 News for specific ticker", placeholder="e.g., AAPL")
        if st.button("Search Ticker News") and ticker_input:
            with st.spinner(f"Fetching news for {ticker_input}..."):
                news = alpha_api.get_financial_news(tickers=ticker_input, limit=5)

                if news:
                    for article in news:
                        st.markdown(f"""
                        <div style='background: #1a1a1a; padding: 15px; border-radius: 8px;
                                    margin-bottom: 10px; border-left: 3px solid #DC143C;'>
                            <h4 style='color: #DC143C; margin: 0 0 10px 0;'>{article.get('title', 'No Title')}</h4>
                            <p style='color: #ccc; margin: 0 0 10px 0;'>{article.get('summary', 'No summary available')[:200]}...</p>
                            <small style='color: #888;'>Relevance: {article.get('relevance_score', 'N/A')}</small>
                        </div>
                        """, unsafe_allow_html=True)