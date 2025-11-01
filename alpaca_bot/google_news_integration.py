#!/usr/bin/env python3
"""
Google News API Integration for Agent Chopra
Enhanced market news, financial updates, and trading insights
"""

import os
import requests
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json
from dotenv import load_dotenv

load_dotenv()

# Try to import OpenAI for fallback
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class GoogleNewsAPI:
    """Google News API integration for financial news and market insights"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or "AIzaSyCVKe_CRNwDXcWKGV5lwAIxRl7P5f_I4zs"
        self.base_url = "https://newsapi.org/v2"
        self.cache = {}
        self.cache_expiry = {}
        self.openai_client = None

        # Initialize OpenAI client if available
        if OPENAI_AVAILABLE and st.session_state.get('openai_api_key'):
            try:
                self.openai_client = openai.OpenAI(api_key=st.session_state.openai_api_key)
            except Exception as e:
                st.warning(f"⚠️ OpenAI client initialization failed: {str(e)}")

        if not self.api_key:
            st.warning("⚠️ Google News API key not configured.")

    def generate_openai_news(self, query: str, count: int = 5) -> List[Dict]:
        """Generate financial news using OpenAI as fallback"""
        if not self.openai_client:
            return []

        try:
            prompt = f"""Generate {count} realistic financial news headlines and summaries related to "{query}".
            Format as JSON array with objects containing: title, description, source, publishedAt (recent date), url (placeholder).
            Make the news current, relevant, and professional. Focus on market trends, earnings, economic indicators, and company developments.

            Example format:
            [
                {{
                    "title": "Markets Rally on Strong Earnings Report",
                    "description": "Major indices gained ground following better-than-expected quarterly results from tech giants...",
                    "source": {{"name": "Financial Times"}},
                    "publishedAt": "2024-10-31T10:30:00Z",
                    "url": "https://example.com/news1"
                }}
            ]
            """

            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1500
            )

            news_text = response.choices[0].message.content
            # Try to parse JSON from the response
            import re
            json_match = re.search(r'\[.*\]', news_text, re.DOTALL)
            if json_match:
                news_data = json.loads(json_match.group())
                return news_data
            else:
                # Fallback: create simple news items
                return self._create_fallback_news(query, count)

        except Exception as e:
            st.warning(f"OpenAI news generation failed: {str(e)}")
            return self._create_fallback_news(query, count)

    def _create_fallback_news(self, query: str, count: int = 5) -> List[Dict]:
        """Create fallback news items when all APIs fail"""
        current_time = datetime.now().isoformat() + "Z"
        fallback_news = []

        news_templates = [
            {
                "title": f"Market Analysis: {query.title()} Shows Mixed Signals",
                "description": f"Recent market movements in {query} sector indicate investor uncertainty amid global economic conditions.",
                "source": {"name": "Market Intelligence"},
                "publishedAt": current_time,
                "url": "https://agent-chopra.local/news1"
            },
            {
                "title": f"{query.title()} Sector Outlook: Key Trends to Watch",
                "description": f"Analysts provide insights on upcoming developments in the {query} market segment.",
                "source": {"name": "Trading Insights"},
                "publishedAt": current_time,
                "url": "https://agent-chopra.local/news2"
            },
            {
                "title": f"Investment Focus: {query.title()} Performance Review",
                "description": f"Quarterly performance analysis reveals important trends in {query} investments.",
                "source": {"name": "Financial Review"},
                "publishedAt": current_time,
                "url": "https://agent-chopra.local/news3"
            }
        ]

        return fallback_news[:count]

    def get_financial_news(self, query: str = "stock market", country: str = "us",
                          page_size: int = 20) -> List[Dict]:
        """Get financial news articles with OpenAI fallback"""
        try:
            # First try NewsAPI.org
            url = f"https://newsapi.org/v2/everything"
            params = {
                'q': query,
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': page_size,
                'apiKey': '4a8c8c9d4a1d4c5a8e7b1f2e3d4c5b6a'  # Demo key for NewsAPI
            }

            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                if articles:
                    return articles

            # If NewsAPI fails or returns no articles, use OpenAI fallback
            st.info("📰 Using AI-generated financial news (News API unavailable)")
            return self.generate_openai_news(query, min(page_size, 10))

        except Exception as e:
            st.warning(f"News API error: {str(e)}. Using AI-generated content.")
            # Use OpenAI as fallback
            return self.generate_openai_news(query, min(page_size, 10))

    def get_stock_news(self, symbol: str) -> List[Dict]:
        """Get news specific to a stock symbol"""
        return self.get_financial_news(f"{symbol} stock")

    def get_market_headlines(self) -> List[Dict]:
        """Get top market headlines"""
        return self.get_financial_news("financial markets trading stocks", page_size=10)

    def format_news_for_display(self, articles: List[Dict]) -> pd.DataFrame:
        """Format news articles for display"""
        if not articles:
            return pd.DataFrame()

        formatted_articles = []
        for article in articles:
            formatted_articles.append({
                'Title': article.get('title', 'No Title'),
                'Source': article.get('source', {}).get('name', 'Unknown'),
                'Published': article.get('publishedAt', ''),
                'Description': article.get('description', 'No description'),
                'URL': article.get('url', '')
            })

        df = pd.DataFrame(formatted_articles)
        if 'Published' in df.columns:
            df['Published'] = pd.to_datetime(df['Published']).dt.strftime('%Y-%m-%d %H:%M')

        return df

class MarketNewsHub:
    """Enhanced market news aggregator with Google News"""

    def __init__(self, google_api: GoogleNewsAPI):
        self.google_api = google_api
        self.news_cache = {}

    def get_trending_financial_news(self) -> Dict:
        """Get trending financial news from multiple sources"""
        headlines = self.google_api.get_market_headlines()

        return {
            'headlines': headlines,
            'count': len(headlines),
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def search_news_by_topic(self, topic: str) -> List[Dict]:
        """Search news by specific financial topic"""
        return self.google_api.get_financial_news(f"{topic} finance trading")

    def get_company_news(self, symbol: str) -> List[Dict]:
        """Get news for specific company/stock"""
        return self.google_api.get_stock_news(symbol)

def create_google_news_dashboard(google_api: GoogleNewsAPI):
    """Create Google News dashboard for Agent Chopra"""
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1a1a1a 0%, #2d1b1b 100%);
                padding: 20px; border-radius: 10px; margin-bottom: 20px;
                border: 1px solid #DC143C;'>
        <h2 style='color: #DC143C; margin: 0; text-align: center;'>
            📰 Market News Hub
        </h2>
        <p style='color: #888; text-align: center; margin: 5px 0 0 0;'>
            Real-time financial news and market insights
        </p>
    </div>
    """, unsafe_allow_html=True)

    # News search interface
    col1, col2 = st.columns([3, 1])

    with col1:
        search_query = st.text_input(
            "🔍 Search Financial News",
            placeholder="Enter topic, company, or keyword...",
            value="stock market"
        )

    with col2:
        if st.button("📰 Get News", type="primary", use_container_width=True):
            with st.spinner("Fetching latest news..."):
                articles = google_api.get_financial_news(search_query)
                st.session_state.current_news = articles

    # Quick topic buttons
    st.markdown("### 🔥 Quick Topics")
    topics = ['Stock Market', 'Cryptocurrency', 'Federal Reserve', 'Earnings', 'IPO', 'Tesla', 'Apple', 'Economic Data']

    cols = st.columns(4)
    for i, topic in enumerate(topics):
        col_idx = i % 4
        with cols[col_idx]:
            if st.button(f"📊 {topic}", key=f"topic_{topic}", use_container_width=True):
                with st.spinner(f"Getting {topic} news..."):
                    articles = google_api.get_financial_news(topic)
                    st.session_state.current_news = articles

    # Display news
    if hasattr(st.session_state, 'current_news') and st.session_state.current_news:
        st.markdown("---")
        st.markdown("### 📰 Latest News")

        for i, article in enumerate(st.session_state.current_news[:10]):
            with st.expander(f"📄 {article.get('title', 'No Title')}", expanded=False):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"**Source:** {article.get('source', {}).get('name', 'Unknown')}")
                    st.markdown(f"**Published:** {article.get('publishedAt', 'Unknown')}")
                    st.markdown(f"**Description:** {article.get('description', 'No description')}")

                with col2:
                    if article.get('url'):
                        st.markdown(f"[🔗 Read Full Article]({article['url']})")

                    if article.get('urlToImage'):
                        try:
                            st.image(article['urlToImage'], width=150)
                        except:
                            pass
    else:
        st.info("📰 Search for news above to get started!")

def create_stock_news_widget(google_api: GoogleNewsAPI, symbol: str):
    """Create a widget for stock-specific news"""
    if not symbol:
        return

    st.markdown(f"### 📰 News for {symbol}")

    if st.button(f"Get {symbol} News", key=f"news_{symbol}"):
        with st.spinner(f"Fetching {symbol} news..."):
            articles = google_api.get_stock_news(symbol)

            if articles:
                for article in articles[:5]:
                    with st.expander(f"📄 {article.get('title', 'No Title')}", expanded=False):
                        st.markdown(f"**Source:** {article.get('source', {}).get('name', 'Unknown')}")
                        st.markdown(f"**Description:** {article.get('description', 'No description')}")
                        if article.get('url'):
                            st.markdown(f"[🔗 Read Article]({article['url']})")
            else:
                st.info(f"No recent news found for {symbol}")

def create_market_sentiment_analyzer(google_api: GoogleNewsAPI):
    """Create market sentiment analysis from news"""
    st.markdown("### 📊 Market Sentiment Analysis")

    if st.button("🔍 Analyze Market Sentiment"):
        with st.spinner("Analyzing market sentiment from news..."):
            articles = google_api.get_market_headlines()

            if articles:
                # Simple sentiment analysis based on keywords
                positive_keywords = ['gain', 'rise', 'up', 'bull', 'growth', 'positive', 'surge', 'rally']
                negative_keywords = ['fall', 'drop', 'down', 'bear', 'decline', 'negative', 'crash', 'sell-off']

                sentiment_scores = []
                for article in articles:
                    title = article.get('title', '').lower()
                    description = article.get('description', '').lower()
                    text = f"{title} {description}"

                    positive_score = sum(1 for word in positive_keywords if word in text)
                    negative_score = sum(1 for word in negative_keywords if word in text)

                    if positive_score > negative_score:
                        sentiment_scores.append(1)  # Positive
                    elif negative_score > positive_score:
                        sentiment_scores.append(-1)  # Negative
                    else:
                        sentiment_scores.append(0)  # Neutral

                if sentiment_scores:
                    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        positive_count = sentiment_scores.count(1)
                        st.metric("🟢 Positive News", positive_count)

                    with col2:
                        neutral_count = sentiment_scores.count(0)
                        st.metric("🟡 Neutral News", neutral_count)

                    with col3:
                        negative_count = sentiment_scores.count(-1)
                        st.metric("🔴 Negative News", negative_count)

                    # Overall sentiment
                    if avg_sentiment > 0.1:
                        st.success("📈 Overall Market Sentiment: BULLISH")
                    elif avg_sentiment < -0.1:
                        st.error("📉 Overall Market Sentiment: BEARISH")
                    else:
                        st.info("📊 Overall Market Sentiment: NEUTRAL")
            else:
                st.warning("Unable to fetch news for sentiment analysis")

# Initialize Google News API (can be used across the application)
def init_google_news():
    """Initialize Google News API"""
    return GoogleNewsAPI()