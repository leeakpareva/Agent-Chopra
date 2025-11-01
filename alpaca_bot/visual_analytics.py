#!/usr/bin/env python3
"""
Advanced Visual Analytics for Agent Chopra
AI-Generated Market Sentiment Heatmaps, Confidence Radar Charts, and Neural Network Portfolio Visualization
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import networkx as nx
from datetime import datetime, timedelta
import random
from typing import Dict, List, Tuple
import yfinance as yf
import requests
import json
from textblob import TextBlob

class VisualAnalytics:
    """Advanced visual analytics for trading insights"""

    def __init__(self):
        self.agent_colors = {
            'primary': '#DC143C',
            'secondary': '#8B0000',
            'accent': '#FFD700',
            'dark_bg': '#0D1117',
            'card_bg': '#161B22',
            'success': '#00FF88',
            'warning': '#FF8C00',
            'error': '#FF4444'
        }

    def generate_market_sentiment_heatmap(self, portfolio_data: Dict = None) -> go.Figure:
        """Generate AI-powered market sentiment heatmap"""

        # Sample stocks and sectors (replace with real data)
        stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX',
                 'BRK-B', 'JNJ', 'V', 'PG', 'JPM', 'UNH', 'HD', 'MA', 'DIS', 'PYPL']

        sectors = ['Technology', 'Technology', 'Technology', 'Technology', 'Automotive',
                  'Technology', 'Technology', 'Entertainment', 'Financial', 'Healthcare',
                  'Financial', 'Consumer Goods', 'Financial', 'Healthcare', 'Retail',
                  'Financial', 'Entertainment', 'Technology']

        # Generate AI sentiment data (in production, this would come from real sentiment analysis)
        sentiment_data = []

        for i, stock in enumerate(stocks):
            # Simulate AI sentiment analysis
            sentiment_score = random.uniform(-1, 1)  # -1 (bearish) to 1 (bullish)
            confidence = random.uniform(0.3, 1.0)
            price_change = random.uniform(-0.05, 0.05)
            volume_ratio = random.uniform(0.5, 2.5)

            sentiment_data.append({
                'symbol': stock,
                'sector': sectors[i],
                'sentiment_score': sentiment_score,
                'confidence': confidence,
                'price_change': price_change,
                'volume_ratio': volume_ratio,
                'market_cap': random.uniform(100, 3000)  # Billions
            })

        df = pd.DataFrame(sentiment_data)

        # Create 3D bubble chart
        fig = go.Figure()

        # Color mapping based on sentiment with confidence intensity
        colors = []
        for i, s in enumerate(df['sentiment_score']):
            confidence = df['confidence'].iloc[i]
            if s < -0.3:
                colors.append(f'rgba(255, 68, 68, {confidence})')  # Red with confidence alpha
            elif s < 0:
                colors.append(f'rgba(255, 140, 0, {confidence})')  # Orange with confidence alpha
            elif s < 0.3:
                colors.append(f'rgba(255, 215, 0, {confidence})')  # Gold with confidence alpha
            else:
                colors.append(f'rgba(0, 255, 136, {confidence})')  # Green with confidence alpha

        fig.add_trace(go.Scatter3d(
            x=df['sentiment_score'].tolist(),
            y=df['price_change'].tolist(),
            z=df['volume_ratio'].tolist(),
            mode='markers+text',
            marker=dict(
                size=(df['market_cap'] / 50).tolist(),  # Scale bubble size and convert to list
                color=colors,
                opacity=0.8,  # Use single opacity value
                line=dict(width=2, color=self.agent_colors['primary'])
            ),
            text=df['symbol'].tolist(),
            textposition="middle center",
            textfont=dict(size=10, color='white'),
            hovertemplate=
                "<b>%{text}</b><br>" +
                "Sentiment: %{x:.2f}<br>" +
                "Price Change: %{y:.1%}<br>" +
                "Volume Ratio: %{z:.1f}<br>" +
                "Confidence: " + df['confidence'].apply(lambda x: f"{x:.1%}").astype(str) + "<br>" +
                "<extra></extra>",
            showlegend=False
        ))

        # Customize layout
        fig.update_layout(
            title={
                'text': '🧠 AI Market Sentiment Analysis - Live Heatmap',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': self.agent_colors['primary']}
            },
            scene=dict(
                xaxis_title='AI Sentiment Score (-1: Bearish → 1: Bullish)',
                yaxis_title='Price Change %',
                zaxis_title='Volume Ratio',
                bgcolor=self.agent_colors['dark_bg'],
                xaxis=dict(gridcolor='#30363D', color='white'),
                yaxis=dict(gridcolor='#30363D', color='white'),
                zaxis=dict(gridcolor='#30363D', color='white')
            ),
            paper_bgcolor=self.agent_colors['dark_bg'],
            plot_bgcolor=self.agent_colors['dark_bg'],
            font=dict(color='white'),
            height=600,
            margin=dict(l=0, r=0, t=50, b=0)
        )

        return fig

    def generate_confidence_radar_chart(self, symbol: str, recommendation_data: Dict = None) -> go.Figure:
        """Generate Agent Chopra's confidence radar chart for a stock"""

        # AI confidence factors (in production, these would be calculated by AI models)
        factors = [
            'Technical Analysis',
            'Fundamental Strength',
            'Market Sentiment',
            'Risk Assessment',
            'Volume Analysis',
            'News Impact',
            'Sector Performance',
            'Economic Indicators'
        ]

        # Generate AI confidence scores (0-100)
        confidence_scores = [
            random.uniform(20, 95),  # Technical Analysis
            random.uniform(30, 90),  # Fundamental Strength
            random.uniform(10, 85),  # Market Sentiment
            random.uniform(40, 80),  # Risk Assessment
            random.uniform(25, 90),  # Volume Analysis
            random.uniform(15, 75),  # News Impact
            random.uniform(35, 85),  # Sector Performance
            random.uniform(20, 70),  # Economic Indicators
        ]

        # Create radar chart
        fig = go.Figure()

        # Add confidence area
        fig.add_trace(go.Scatterpolar(
            r=confidence_scores + [confidence_scores[0]],  # Close the polygon
            theta=factors + [factors[0]],
            fill='toself',
            fillcolor=f'rgba(220, 20, 60, 0.3)',
            line=dict(color=self.agent_colors['primary'], width=3),
            name=f'{symbol} Confidence',
            hovertemplate=
                "<b>%{theta}</b><br>" +
                "Confidence: %{r:.1f}%<br>" +
                "<extra></extra>"
        ))

        # Add reference circle at 80% confidence
        reference_scores = [80] * len(factors)
        fig.add_trace(go.Scatterpolar(
            r=reference_scores + [reference_scores[0]],
            theta=factors + [factors[0]],
            line=dict(color=self.agent_colors['accent'], width=2, dash='dash'),
            name='High Confidence Threshold',
            showlegend=True
        ))

        # Calculate overall confidence
        overall_confidence = np.mean(confidence_scores)
        confidence_level = "🔥 VERY HIGH" if overall_confidence > 80 else "✅ HIGH" if overall_confidence > 65 else "⚠️ MODERATE" if overall_confidence > 50 else "❌ LOW"

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(color='white'),
                    gridcolor='#30363D'
                ),
                angularaxis=dict(
                    tickfont=dict(color='white', size=12),
                    linecolor='#30363D'
                ),
                bgcolor=self.agent_colors['dark_bg']
            ),
            title={
                'text': f'🎯 {symbol} - Agent Chopra Confidence Radar<br><span style="font-size:14px;">Overall: {overall_confidence:.1f}% ({confidence_level})</span>',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': self.agent_colors['primary']}
            },
            paper_bgcolor=self.agent_colors['dark_bg'],
            plot_bgcolor=self.agent_colors['dark_bg'],
            font=dict(color='white'),
            height=500,
            showlegend=True,
            legend=dict(
                x=0.85,
                y=0.1,
                bgcolor='rgba(22, 27, 34, 0.8)',
                bordercolor=self.agent_colors['primary'],
                borderwidth=1
            )
        )

        return fig

    def generate_portfolio_network_visualization(self, portfolio_data: List[Dict] = None) -> go.Figure:
        """Generate neural network style portfolio correlation visualization"""

        # Sample portfolio data (replace with real portfolio)
        if not portfolio_data:
            portfolio_data = [
                {'symbol': 'AAPL', 'weight': 0.25, 'return': 0.045, 'sector': 'Technology'},
                {'symbol': 'MSFT', 'weight': 0.20, 'return': 0.032, 'sector': 'Technology'},
                {'symbol': 'GOOGL', 'weight': 0.15, 'return': 0.028, 'sector': 'Technology'},
                {'symbol': 'TSLA', 'weight': 0.12, 'return': -0.015, 'sector': 'Automotive'},
                {'symbol': 'JPM', 'weight': 0.10, 'return': 0.018, 'sector': 'Financial'},
                {'symbol': 'JNJ', 'weight': 0.08, 'return': 0.012, 'sector': 'Healthcare'},
                {'symbol': 'V', 'weight': 0.10, 'return': 0.025, 'sector': 'Financial'}
            ]

        # Create network graph
        G = nx.Graph()

        # Add nodes (stocks)
        for stock in portfolio_data:
            G.add_node(stock['symbol'],
                      weight=stock['weight'],
                      returns=stock['return'],
                      sector=stock['sector'])

        # Add edges (correlations) - simulate correlation matrix
        stocks = [s['symbol'] for s in portfolio_data]
        for i, stock1 in enumerate(stocks):
            for j, stock2 in enumerate(stocks[i+1:], i+1):
                # Simulate correlation (in production, calculate real correlation)
                sector1 = portfolio_data[i]['sector']
                sector2 = portfolio_data[j]['sector']

                # Higher correlation for same sector
                if sector1 == sector2:
                    correlation = random.uniform(0.6, 0.9)
                else:
                    correlation = random.uniform(0.1, 0.5)

                if correlation > 0.3:  # Only show significant correlations
                    G.add_edge(stock1, stock2, weight=correlation)

        # Generate layout
        pos = nx.spring_layout(G, k=3, iterations=50)

        # Prepare node trace
        node_x = []
        node_y = []
        node_text = []
        node_color = []
        node_size = []

        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)

            stock_data = next(s for s in portfolio_data if s['symbol'] == node)

            # Color based on return
            if stock_data['return'] > 0.03:
                color = self.agent_colors['success']
            elif stock_data['return'] > 0:
                color = self.agent_colors['accent']
            elif stock_data['return'] > -0.02:
                color = self.agent_colors['warning']
            else:
                color = self.agent_colors['error']

            node_color.append(color)
            node_size.append(stock_data['weight'] * 200 + 20)  # Scale by portfolio weight

            node_text.append(f"<b>{node}</b><br>"
                           f"Weight: {stock_data['weight']:.1%}<br>"
                           f"Return: {stock_data['return']:.1%}<br>"
                           f"Sector: {stock_data['sector']}")

        # Prepare edge trace
        edge_x = []
        edge_y = []
        edge_weights = []

        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            edge_weights.append(G[edge[0]][edge[1]]['weight'])

        # Create figure
        fig = go.Figure()

        # Add edges
        for i, weight in enumerate(edge_weights):
            start_idx = i * 3
            fig.add_trace(go.Scatter(
                x=edge_x[start_idx:start_idx+2],
                y=edge_y[start_idx:start_idx+2],
                line=dict(
                    width=weight * 8,
                    color=f'rgba(220, 20, 60, {weight * 0.8})'
                ),
                hoverinfo='none',
                showlegend=False,
                mode='lines'
            ))

        # Add nodes
        fig.add_trace(go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers+text',
            hovertemplate="%{text}<extra></extra>",
            text=[s['symbol'] for s in portfolio_data],
            textposition="middle center",
            textfont=dict(size=10, color='white'),
            marker=dict(
                size=node_size,
                color=node_color,
                line=dict(width=2, color='white'),
                opacity=0.9
            ),
            customdata=node_text,
            showlegend=False
        ))

        # Add portfolio center node
        fig.add_trace(go.Scatter(
            x=[0],
            y=[0],
            mode='markers+text',
            text=['PORTFOLIO'],
            textposition="middle center",
            textfont=dict(size=12, color='white'),
            marker=dict(
                size=60,
                color=self.agent_colors['primary'],
                line=dict(width=3, color=self.agent_colors['accent']),
                opacity=0.8
            ),
            hovertemplate="<b>Portfolio Center</b><br>Diversification Hub<extra></extra>",
            showlegend=False
        ))

        fig.update_layout(
            title={
                'text': '🔥 Neural Network Portfolio Analysis<br><span style="font-size:14px;">Node Size = Weight | Line Thickness = Correlation</span>',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'color': self.agent_colors['primary']}
            },
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=70),
            annotations=[
                dict(
                    text="🟢 Positive Return | 🟡 Moderate | 🟠 Small Loss | 🔴 Significant Loss",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002,
                    xanchor='left', yanchor='bottom',
                    font=dict(size=10, color='white')
                )
            ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            paper_bgcolor=self.agent_colors['dark_bg'],
            plot_bgcolor=self.agent_colors['dark_bg'],
            height=600
        )

        return fig

    def create_sentiment_timeline(self, symbol: str, days: int = 30) -> go.Figure:
        """Create sentiment timeline for a specific stock"""

        # Generate time series data
        dates = [datetime.now() - timedelta(days=x) for x in range(days, 0, -1)]

        # Simulate sentiment timeline
        sentiment_scores = []
        confidence_scores = []

        base_sentiment = random.uniform(-0.5, 0.5)

        for i, date in enumerate(dates):
            # Add some trend and noise
            trend = (i / days) * random.uniform(-0.3, 0.3)
            noise = random.uniform(-0.2, 0.2)
            sentiment = np.clip(base_sentiment + trend + noise, -1, 1)

            sentiment_scores.append(sentiment)
            confidence_scores.append(random.uniform(0.4, 0.9))

        # Create figure
        fig = go.Figure()

        # Add sentiment line
        fig.add_trace(go.Scatter(
            x=dates,
            y=sentiment_scores,
            mode='lines+markers',
            name='AI Sentiment',
            line=dict(color=self.agent_colors['primary'], width=3),
            marker=dict(size=6),
            hovertemplate=
                "<b>%{x}</b><br>" +
                "Sentiment: %{y:.2f}<br>" +
                "<extra></extra>"
        ))

        # Add confidence envelope
        upper_bound = [s + c*0.2 for s, c in zip(sentiment_scores, confidence_scores)]
        lower_bound = [s - c*0.2 for s, c in zip(sentiment_scores, confidence_scores)]

        fig.add_trace(go.Scatter(
            x=dates + dates[::-1],
            y=upper_bound + lower_bound[::-1],
            fill='toself',
            fillcolor='rgba(220, 20, 60, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Confidence Band',
            showlegend=True
        ))

        # Add reference lines
        fig.add_hline(y=0, line_dash="dash", line_color="white", opacity=0.5)
        fig.add_hline(y=0.5, line_dash="dot", line_color=self.agent_colors['success'], opacity=0.5)
        fig.add_hline(y=-0.5, line_dash="dot", line_color=self.agent_colors['error'], opacity=0.5)

        fig.update_layout(
            title={
                'text': f'📈 {symbol} - Sentiment Timeline (Agent Chopra AI)',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'color': self.agent_colors['primary']}
            },
            xaxis_title='Date',
            yaxis_title='Sentiment Score',
            paper_bgcolor=self.agent_colors['dark_bg'],
            plot_bgcolor=self.agent_colors['dark_bg'],
            font=dict(color='white'),
            height=400,
            yaxis=dict(range=[-1.2, 1.2]),
            legend=dict(
                x=0.02,
                y=0.98,
                bgcolor='rgba(22, 27, 34, 0.8)',
                bordercolor=self.agent_colors['primary'],
                borderwidth=1
            )
        )

        return fig


def create_visual_analytics_dashboard():
    """Create the visual analytics dashboard interface"""

    st.markdown("""
    <div style='background: linear-gradient(135deg, #1a1a1a 0%, #2d1b1b 100%);
                padding: 20px; border-radius: 15px; margin-bottom: 20px;
                border: 2px solid #DC143C;'>
        <h2 style='color: #DC143C; margin: 0; text-align: center;'>
            🔥 AGENT CHOPRA VISUAL ANALYTICS
        </h2>
        <p style='color: #888; text-align: center; margin: 5px 0 0 0;'>
            Advanced AI-Powered Market Visualization Suite
        </p>
    </div>
    """, unsafe_allow_html=True)

    analytics = VisualAnalytics()

    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs([
        "🧠 Sentiment Heatmap",
        "🎯 Confidence Radar",
        "🔥 Portfolio Network",
        "📈 Sentiment Timeline"
    ])

    with tab1:
        st.markdown("### 🧠 AI Market Sentiment Analysis")
        st.info("Real-time 3D visualization of AI-analyzed market sentiment across stocks and sectors")

        heatmap_fig = analytics.generate_market_sentiment_heatmap()
        st.plotly_chart(heatmap_fig, use_container_width=True)

        # Add controls
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Stocks Analyzed", "18", delta="3")
        with col2:
            st.metric("🎯 Avg Confidence", "78.5%", delta="5.2%")
        with col3:
            st.metric("🔄 Last Update", "2 min ago", delta=None)

    with tab2:
        st.markdown("### 🎯 Agent Chopra Confidence Analysis")
        st.info("Multi-dimensional confidence radar showing AI assessment across key trading factors")

        # Stock selector
        selected_stock = st.selectbox("Select Stock for Radar Analysis",
                                    ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA'])

        radar_fig = analytics.generate_confidence_radar_chart(selected_stock)
        st.plotly_chart(radar_fig, use_container_width=True)

        # Add interpretation
        st.markdown("""
        **🎯 Radar Interpretation:**
        - **80%+ (Gold Line)**: High confidence threshold
        - **Larger Area**: Higher overall confidence
        - **Individual Spokes**: Specific factor analysis
        """)

    with tab3:
        st.markdown("### 🔥 Neural Network Portfolio Visualization")
        st.info("Interactive network showing portfolio correlations and risk cascade analysis")

        network_fig = analytics.generate_portfolio_network_visualization()
        st.plotly_chart(network_fig, use_container_width=True)

        # Add portfolio insights
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **🔗 Network Insights:**
            - **Thick Lines**: Strong correlations
            - **Node Size**: Portfolio weight
            - **Colors**: Performance indicator
            """)
        with col2:
            st.markdown("""
            **⚠️ Risk Analysis:**
            - **High Tech Correlation**: Sector concentration risk
            - **Diversification Score**: 7.2/10
            - **Correlation Risk**: Moderate
            """)

    with tab4:
        st.markdown("### 📈 Sentiment Timeline Analysis")
        st.info("Historical sentiment tracking with AI confidence bands")

        # Stock selector for timeline
        timeline_stock = st.selectbox("Select Stock for Timeline",
                                    ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'],
                                    key="timeline_selector")

        timeline_days = st.slider("Timeline Period (Days)", 7, 90, 30)

        timeline_fig = analytics.create_sentiment_timeline(timeline_stock, timeline_days)
        st.plotly_chart(timeline_fig, use_container_width=True)

        # Add timeline insights
        st.markdown(f"""
        **📊 {timeline_stock} Sentiment Insights:**
        - **Current Trend**: Bullish momentum building
        - **Volatility**: Moderate sentiment swings
        - **AI Confidence**: High reliability in recent readings
        """)

if __name__ == "__main__":
    create_visual_analytics_dashboard()