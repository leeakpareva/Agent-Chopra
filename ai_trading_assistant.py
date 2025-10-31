#!/usr/bin/env python3
"""
AI Trading Assistant with RAG Capabilities
Intelligent assistant that analyzes trading activities and provides insights
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import pandas as pd
from dotenv import load_dotenv

# LangChain imports
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory

# Alpaca imports
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import QueryOrderStatus

load_dotenv()

class TradingDataCollector:
    """Collects and stores trading data for RAG"""

    def __init__(self, db_path: str = "trading_data.db"):
        self.db_path = db_path
        self.client = None
        self._init_database()
        self._init_alpaca_client()

    def _init_database(self):
        """Initialize SQLite database for trading data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id TEXT PRIMARY KEY,
                symbol TEXT,
                side TEXT,
                quantity INTEGER,
                price REAL,
                status TEXT,
                submitted_at TEXT,
                filled_at TEXT,
                filled_qty INTEGER,
                order_type TEXT,
                created_at TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS positions (
                symbol TEXT PRIMARY KEY,
                quantity REAL,
                avg_entry_price REAL,
                current_price REAL,
                market_value REAL,
                unrealized_pl REAL,
                unrealized_plpc REAL,
                updated_at TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS account_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                portfolio_value REAL,
                buying_power REAL,
                cash REAL,
                day_trading_buying_power REAL,
                positions_count INTEGER,
                created_at TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def _init_alpaca_client(self):
        """Initialize Alpaca client"""
        try:
            api_key = os.getenv('APCA_API_KEY_ID')
            api_secret = os.getenv('APCA_API_SECRET_KEY')

            if api_key and api_secret:
                self.client = TradingClient(
                    api_key=api_key,
                    secret_key=api_secret,
                    paper=True
                )
        except Exception as e:
            print(f"Warning: Could not initialize Alpaca client: {e}")

    def collect_and_store_data(self):
        """Collect current trading data and store in database"""
        if not self.client:
            return

        try:
            # Get and store account data
            account = self.client.get_account()
            positions = self.client.get_all_positions()

            # Get recent orders
            request = GetOrdersRequest(
                status=QueryOrderStatus.ALL,
                limit=100,
                nested=False
            )
            orders = self.client.get_orders(filter=request)

            # Store in database
            self._store_account_snapshot(account, len(positions))
            self._store_positions(positions)
            self._store_orders(orders)

        except Exception as e:
            print(f"Error collecting trading data: {e}")

    def _store_account_snapshot(self, account, positions_count):
        """Store account snapshot"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO account_snapshots
            (portfolio_value, buying_power, cash, day_trading_buying_power, positions_count, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            float(account.equity),
            float(account.buying_power),
            float(account.cash),
            float(account.daytrading_buying_power) if account.daytrading_buying_power else 0,
            positions_count,
            datetime.now().isoformat()
        ))

        conn.commit()
        conn.close()

    def _store_positions(self, positions):
        """Store current positions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for pos in positions:
            cursor.execute('''
                INSERT OR REPLACE INTO positions
                (symbol, quantity, avg_entry_price, current_price, market_value,
                 unrealized_pl, unrealized_plpc, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                pos.symbol,
                float(pos.qty),
                float(pos.avg_entry_price),
                float(pos.current_price) if pos.current_price else 0,
                float(pos.market_value),
                float(pos.unrealized_pl) if pos.unrealized_pl else 0,
                float(pos.unrealized_plpc) if pos.unrealized_plpc else 0,
                datetime.now().isoformat()
            ))

        conn.commit()
        conn.close()

    def _store_orders(self, orders):
        """Store orders"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for order in orders:
            cursor.execute('''
                INSERT OR REPLACE INTO trades
                (id, symbol, side, quantity, price, status, submitted_at,
                 filled_at, filled_qty, order_type, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                str(order.id),
                order.symbol,
                str(order.side),
                order.qty,
                float(order.limit_price) if order.limit_price else 0,
                str(order.status),
                str(order.submitted_at),
                str(order.filled_at) if order.filled_at else None,
                order.filled_qty if order.filled_qty else 0,
                str(order.order_type),
                datetime.now().isoformat()
            ))

        conn.commit()
        conn.close()

    def get_trading_summary(self, days: int = 30) -> str:
        """Get trading summary as text for RAG"""
        conn = sqlite3.connect(self.db_path)

        # Get recent data
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()

        # Trades summary
        trades_df = pd.read_sql_query('''
            SELECT * FROM trades
            WHERE created_at > ?
            ORDER BY submitted_at DESC
        ''', conn, params=[cutoff_date])

        # Account snapshots
        account_df = pd.read_sql_query('''
            SELECT * FROM account_snapshots
            WHERE created_at > ?
            ORDER BY created_at DESC
        ''', conn, params=[cutoff_date])

        # Current positions
        positions_df = pd.read_sql_query('''
            SELECT * FROM positions
            ORDER BY updated_at DESC
        ''', conn)

        conn.close()

        # Generate summary text
        summary = f"""
        TRADING ACTIVITY SUMMARY (Last {days} days)
        Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        ACCOUNT OVERVIEW:
        """

        if not account_df.empty:
            latest_account = account_df.iloc[0]
            summary += f"""
        - Current Portfolio Value: ${latest_account['portfolio_value']:,.2f}
        - Available Cash: ${latest_account['cash']:,.2f}
        - Buying Power: ${latest_account['buying_power']:,.2f}
        - Number of Positions: {latest_account['positions_count']}
        """

        summary += "\n        RECENT TRADES:\n"
        if not trades_df.empty:
            for _, trade in trades_df.head(20).iterrows():
                summary += f"""
        - {trade['submitted_at'][:10]}: {trade['side'].upper()} {trade['quantity']} {trade['symbol']}
          Status: {trade['status']}, Type: {trade['order_type']}
        """
        else:
            summary += "        - No recent trades found\n"

        summary += "\n        CURRENT POSITIONS:\n"
        if not positions_df.empty:
            total_unrealized_pl = positions_df['unrealized_pl'].sum()
            for _, pos in positions_df.iterrows():
                pnl_pct = pos['unrealized_plpc'] * 100 if pos['unrealized_plpc'] else 0
                summary += f"""
        - {pos['symbol']}: {pos['quantity']} shares @ ${pos['avg_entry_price']:.2f}
          Current: ${pos['current_price']:.2f}, P/L: ${pos['unrealized_pl']:.2f} ({pnl_pct:.2f}%)
        """
            summary += f"\n        Total Unrealized P/L: ${total_unrealized_pl:.2f}\n"
        else:
            summary += "        - No open positions\n"

        # Trading performance analysis
        if not trades_df.empty:
            filled_trades = trades_df[trades_df['status'] == 'filled']
            total_trades = len(filled_trades)
            buy_trades = len(filled_trades[filled_trades['side'] == 'buy'])
            sell_trades = len(filled_trades[filled_trades['side'] == 'sell'])

            summary += f"""
        TRADING STATISTICS:
        - Total Executed Trades: {total_trades}
        - Buy Orders: {buy_trades}
        - Sell Orders: {sell_trades}
        - Most Traded Symbol: {trades_df['symbol'].value_counts().index[0] if not trades_df.empty else 'N/A'}
        """

        return summary

class AITradingAssistant:
    """AI Assistant with RAG capabilities for trading analysis"""

    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
        self.data_collector = TradingDataCollector()

        # Initialize components
        self.llm = ChatOpenAI(
            api_key=openai_api_key,
            model="gpt-4o-mini",
            temperature=0.3
        )

        self.embeddings = OpenAIEmbeddings(api_key=openai_api_key)

        # Initialize vector store
        self.vector_store = Chroma(
            persist_directory="./chroma_db",
            embedding_function=self.embeddings
        )

        # Initialize memory
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=10
        )

        # Create system prompt
        self.system_prompt = """You are an intelligent trading assistant with access to detailed trading data and market analysis capabilities.

        Your role is to:
        1. Analyze trading performance and patterns
        2. Provide insights on portfolio optimization
        3. Suggest risk management improvements
        4. Answer questions about trading history and performance
        5. Offer market analysis and trading ideas

        Key guidelines:
        - Always prioritize risk management and responsible trading
        - Provide data-driven insights based on actual trading history
        - Be clear about the limitations of your analysis
        - Remind users this is for paper trading only
        - Use specific numbers and metrics when available

        Remember: This is a paper trading environment - no real money is at risk."""

    def update_knowledge_base(self):
        """Update the RAG knowledge base with latest trading data"""
        try:
            # Collect latest data
            self.data_collector.collect_and_store_data()

            # Get trading summary
            trading_summary = self.data_collector.get_trading_summary(days=90)

            # Create document
            doc = Document(
                page_content=trading_summary,
                metadata={
                    "source": "trading_data",
                    "timestamp": datetime.now().isoformat(),
                    "type": "trading_summary"
                }
            )

            # Split text
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            splits = text_splitter.split_documents([doc])

            # Add to vector store
            self.vector_store.add_documents(splits)

            return True

        except Exception as e:
            print(f"Error updating knowledge base: {e}")
            return False

    def query(self, question: str) -> str:
        """Query the AI assistant with RAG context"""
        try:
            # Update knowledge base with latest data
            self.update_knowledge_base()

            # Retrieve relevant documents
            relevant_docs = self.vector_store.similarity_search(question, k=5)

            # Create context
            context = "\n\n".join([doc.page_content for doc in relevant_docs])

            # Create prompt
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", self.system_prompt),
                ("human", f"""
                Context from trading data:
                {context}

                Question: {question}

                Please provide a comprehensive answer based on the trading data and your analysis capabilities.
                """)
            ])

            # Generate response
            chain = prompt_template | self.llm
            response = chain.invoke({"context": context, "question": question})

            return response.content

        except Exception as e:
            return f"Error processing query: {str(e)}"

    def get_trading_insights(self) -> str:
        """Get automated trading insights"""
        insights_prompt = """
        Based on my recent trading activity and current portfolio:

        1. Analyze my trading performance over the last 30 days
        2. Identify any patterns or trends in my trading behavior
        3. Assess my current portfolio risk and diversification
        4. Provide 3 specific recommendations for improvement
        5. Highlight any potential red flags or areas of concern

        Please be specific and use actual numbers from my trading data.
        """

        return self.query(insights_prompt)

    def analyze_portfolio(self) -> str:
        """Analyze current portfolio composition"""
        portfolio_prompt = """
        Analyze my current portfolio:

        1. Portfolio composition and sector diversification
        2. Position sizing and risk allocation
        3. Unrealized P/L analysis
        4. Recommendations for rebalancing
        5. Risk assessment and suggestions

        Focus on actionable insights for portfolio optimization.
        """

        return self.query(portfolio_prompt)

    def get_trade_recommendations(self, market_context: str = "") -> str:
        """Get trade recommendations based on analysis"""
        rec_prompt = f"""
        Based on my trading history, current positions, and portfolio analysis:

        Market Context: {market_context}

        Provide:
        1. Specific trading opportunities or adjustments
        2. Position sizing recommendations
        3. Risk management suggestions
        4. Entry/exit strategies for current positions
        5. New investment ideas that fit my trading style

        Be specific and actionable, considering my actual trading patterns.
        """

        return self.query(rec_prompt)

def create_streamlit_ai_interface():
    """Create Streamlit interface for AI assistant"""

    import streamlit as st

    st.title("🤖 AI Trading Assistant")
    st.write("Intelligent analysis of your trading activities with RAG-powered insights")

    # Initialize assistant
    if 'ai_assistant' not in st.session_state:
        openai_key = st.text_input("Enter OpenAI API Key:", type="password")
        if openai_key:
            try:
                st.session_state.ai_assistant = AITradingAssistant(openai_key)
                st.success("AI Assistant initialized successfully!")
            except Exception as e:
                st.error(f"Error initializing AI Assistant: {e}")
                return
        else:
            st.warning("Please enter your OpenAI API key to continue")
            return

    assistant = st.session_state.ai_assistant

    # Tabs for different functions
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📊 Insights", "🎯 Portfolio Analysis", "💡 Recommendations"])

    with tab1:
        st.subheader("Chat with AI Assistant")

        question = st.text_area("Ask a question about your trading:")

        if st.button("Get Answer"):
            if question:
                with st.spinner("Analyzing your trading data..."):
                    response = assistant.query(question)
                    st.write(response)
            else:
                st.warning("Please enter a question")

    with tab2:
        st.subheader("Automated Trading Insights")

        if st.button("Generate Insights"):
            with st.spinner("Analyzing trading performance..."):
                insights = assistant.get_trading_insights()
                st.write(insights)

    with tab3:
        st.subheader("Portfolio Analysis")

        if st.button("Analyze Portfolio"):
            with st.spinner("Analyzing portfolio composition..."):
                analysis = assistant.analyze_portfolio()
                st.write(analysis)

    with tab4:
        st.subheader("Trade Recommendations")

        market_context = st.text_area("Current market context (optional):")

        if st.button("Get Recommendations"):
            with st.spinner("Generating trade recommendations..."):
                recommendations = assistant.get_trade_recommendations(market_context)
                st.write(recommendations)

    # Update knowledge base
    if st.button("🔄 Update Knowledge Base"):
        with st.spinner("Updating trading data..."):
            success = assistant.update_knowledge_base()
            if success:
                st.success("Knowledge base updated successfully!")
            else:
                st.error("Failed to update knowledge base")

if __name__ == "__main__":
    # Test the assistant
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "streamlit":
        create_streamlit_ai_interface()
    else:
        # Command line interface
        openai_key = input("Enter your OpenAI API key: ")
        assistant = AITradingAssistant(openai_key)

        print("AI Trading Assistant initialized!")
        print("Available commands:")
        print("1. 'insights' - Get trading insights")
        print("2. 'portfolio' - Analyze portfolio")
        print("3. 'recommendations' - Get trade recommendations")
        print("4. Or ask any question about your trading")
        print("5. 'quit' - Exit")

        while True:
            user_input = input("\n> ").strip()

            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'insights':
                print("\nGenerating insights...")
                print(assistant.get_trading_insights())
            elif user_input.lower() == 'portfolio':
                print("\nAnalyzing portfolio...")
                print(assistant.analyze_portfolio())
            elif user_input.lower() == 'recommendations':
                print("\nGenerating recommendations...")
                print(assistant.get_trade_recommendations())
            else:
                print("\nProcessing your question...")
                print(assistant.query(user_input))