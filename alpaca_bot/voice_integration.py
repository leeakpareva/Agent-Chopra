#!/usr/bin/env python3
"""
OpenAI Voice Integration for Agent Chopra
Text-to-Speech capabilities with custom prompt integration
"""

import os
import io
import base64
from typing import Optional, Dict
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import tempfile

load_dotenv()

class VoiceAssistant:
    """OpenAI Voice Assistant for Agent Chopra"""

    def __init__(self):
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize OpenAI client with fresh environment variables"""
        # Force reload environment variables
        load_dotenv(override=True)

        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.tts_prompt_id = os.getenv('OPENAI_TTS_PROMPT_ID')

        if self.openai_api_key:
            try:
                self.client = OpenAI(api_key=self.openai_api_key)
            except Exception as e:
                st.error(f"Failed to initialize OpenAI client: {str(e)}")
                self.client = None
        else:
            st.warning("⚠️ OpenAI API key not configured. Voice features will be unavailable.")

    def text_to_speech(self, text: str, voice: str = "alloy", model: str = "tts-1") -> Optional[bytes]:
        """Convert text to speech using OpenAI TTS"""
        if not self.client:
            # Try to re-initialize client in case API key was updated
            self._initialize_client()
            if not self.client:
                return None

        try:
            response = self.client.audio.speech.create(
                model=model,
                voice=voice,
                input=text
            )

            return response.content

        except Exception as e:
            error_msg = str(e)
            st.error(f"OpenAI TTS error: {error_msg}")

            # If it's an API key error, try to reinitialize once
            if "api key" in error_msg.lower() or "401" in error_msg:
                st.info("🔄 Attempting to reload API credentials...")
                self._initialize_client()
                if self.client:
                    try:
                        response = self.client.audio.speech.create(
                            model=model,
                            voice=voice,
                            input=text
                        )
                        return response.content
                    except Exception as retry_e:
                        st.error(f"Retry failed: {str(retry_e)}")

            return None

    def generate_trading_commentary(self, market_data: Dict) -> str:
        """Generate trading commentary using custom prompt"""
        if not self.client:
            # Try to re-initialize client in case API key was updated
            self._initialize_client()
            if not self.client:
                return "Voice assistant unavailable - OpenAI API key not configured."

        try:
            # Enhanced prompt for trading commentary
            system_prompt = f"""
            You are Agent Chopra, an AI trading assistant with a professional yet engaging voice.
            Your role is to provide clear, concise market commentary and trading insights.

            Guidelines:
            - Keep responses under 150 words for voice delivery
            - Use a confident, professional tone
            - Include specific numbers and percentages when available
            - Mention key market drivers and trends
            - End with actionable insights or recommendations
            - Use trading terminology appropriately

            Custom Prompt ID: {self.tts_prompt_id}
            """

            # Format market data for analysis
            market_summary = self._format_market_data(market_data)

            user_prompt = f"""
            Please provide a trading commentary based on this market data:
            {market_summary}

            Focus on:
            1. Current market performance
            2. Key movers and trends
            3. Risk factors to watch
            4. Trading opportunities
            """

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as e:
            st.error(f"OpenAI commentary generation error: {str(e)}")
            return "Unable to generate market commentary at this time."

    def _format_market_data(self, market_data: Dict) -> str:
        """Format market data for commentary generation"""
        if not market_data:
            return "No market data available for analysis."

        formatted = []

        # Portfolio performance
        if 'total_pnl' in market_data:
            pnl = market_data['total_pnl']
            pnl_status = "gains" if pnl >= 0 else "losses"
            formatted.append(f"Portfolio showing ${abs(pnl):,.2f} in {pnl_status}")

        # Individual positions
        if 'positions' in market_data:
            positions = market_data['positions']
            winners = sum(1 for pos in positions if pos.get('pnl', 0) > 0)
            total_positions = len(positions)
            formatted.append(f"{winners} out of {total_positions} positions are profitable")

        # Market sentiment
        if 'market_sentiment' in market_data:
            formatted.append(f"Market sentiment: {market_data['market_sentiment']}")

        # Top performers
        if 'top_performer' in market_data:
            formatted.append(f"Top performer: {market_data['top_performer']}")

        return ". ".join(formatted) if formatted else "Limited market data available."

    def create_audio_player(self, audio_content: bytes, autoplay: bool = False) -> None:
        """Create audio player widget in Streamlit"""
        if not audio_content:
            return

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tmp_file.write(audio_content)
            tmp_file_path = tmp_file.name

        # Read the file and encode it
        with open(tmp_file_path, "rb") as audio_file:
            audio_bytes = audio_file.read()

        # Create audio player
        st.audio(audio_bytes, format="audio/mp3", autoplay=autoplay)

        # Clean up temporary file
        os.unlink(tmp_file_path)

def create_voice_interface():
    """Create the voice interface dashboard"""
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1a1a1a 0%, #2d1b1b 100%);
                padding: 20px; border-radius: 10px; margin-bottom: 20px;
                border: 1px solid #DC143C;'>
        <h2 style='color: #DC143C; margin: 0; text-align: center;'>
            🎤 Agent Chopra Voice Assistant
        </h2>
        <p style='color: #888; text-align: center; margin: 5px 0 0 0;'>
            AI-powered voice commentary and market insights
        </p>
    </div>
    """, unsafe_allow_html=True)

    voice_assistant = VoiceAssistant()

    # Voice settings
    col1, col2, col3 = st.columns(3)

    with col1:
        voice_model = st.selectbox(
            "Voice Model",
            ["tts-1", "tts-1-hd"],
            help="tts-1 is faster, tts-1-hd has higher quality"
        )

    with col2:
        voice_type = st.selectbox(
            "Voice Type",
            ["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
            help="Different voice personalities"
        )

    with col3:
        autoplay = st.checkbox("Auto-play audio", value=False)

    # Voice features tabs
    tab1, tab2, tab3 = st.tabs(["📈 Market Commentary", "💬 Custom Message", "📊 Portfolio Insights"])

    with tab1:
        st.markdown("### 📈 AI Market Commentary")

        # Sample market data (replace with real data from your trading system)
        sample_market_data = {
            'total_pnl': 1250.75,
            'positions': [
                {'symbol': 'AAPL', 'pnl': 340.50},
                {'symbol': 'MSFT', 'pnl': -125.25},
                {'symbol': 'GOOGL', 'pnl': 890.30},
                {'symbol': 'TSLA', 'pnl': 145.20}
            ],
            'market_sentiment': 'Bullish with tech leadership',
            'top_performer': 'GOOGL (+6.7%)'
        }

        if st.button("🎤 Generate Market Commentary", type="primary"):
            with st.spinner("Generating AI commentary..."):
                commentary = voice_assistant.generate_trading_commentary(sample_market_data)

                if commentary:
                    st.markdown("#### 📝 Commentary Text:")
                    st.info(commentary)

                    # Generate audio
                    with st.spinner("Converting to speech..."):
                        audio_content = voice_assistant.text_to_speech(
                            commentary,
                            voice=voice_type,
                            model=voice_model
                        )

                        if audio_content:
                            st.markdown("#### 🔊 Audio Commentary:")
                            voice_assistant.create_audio_player(audio_content, autoplay=autoplay)
                        else:
                            st.error("Failed to generate audio. Please check your OpenAI API configuration.")

    with tab2:
        st.markdown("### 💬 Custom Voice Message")

        custom_text = st.text_area(
            "Enter text to convert to speech",
            placeholder="Type your message here... Agent Chopra will speak it aloud!",
            height=100
        )

        if st.button("🗣️ Speak Message", type="primary") and custom_text:
            with st.spinner("Converting text to speech..."):
                audio_content = voice_assistant.text_to_speech(
                    custom_text,
                    voice=voice_type,
                    model=voice_model
                )

                if audio_content:
                    st.markdown("#### 🔊 Your Message:")
                    voice_assistant.create_audio_player(audio_content, autoplay=autoplay)
                else:
                    st.error("Failed to generate audio. Please check your OpenAI API configuration.")

    with tab3:
        st.markdown("### 📊 Portfolio Voice Insights")

        insight_options = [
            "Daily portfolio performance summary",
            "Top winning and losing positions",
            "Risk assessment and recommendations",
            "Market outlook and strategy",
            "Sector allocation analysis"
        ]

        selected_insight = st.selectbox("Choose insight type", insight_options)

        if st.button("🎯 Generate Insight", type="primary"):
            # Generate insight based on selection
            insight_prompts = {
                "Daily portfolio performance summary": "Provide a comprehensive daily portfolio performance summary including total returns, best and worst performers, and overall market sentiment impact on the portfolio.",
                "Top winning and losing positions": "Analyze the top winning and losing positions in the portfolio, explaining the factors driving their performance and potential next steps.",
                "Risk assessment and recommendations": "Conduct a risk assessment of the current portfolio composition and provide specific recommendations for risk management and optimization.",
                "Market outlook and strategy": "Share the current market outlook and strategic recommendations for portfolio positioning in the upcoming trading sessions.",
                "Sector allocation analysis": "Analyze the current sector allocation in the portfolio and recommend any adjustments based on market trends and economic indicators."
            }

            insight_text = insight_prompts[selected_insight]

            # Add portfolio context
            portfolio_context = """
            Current Portfolio Context:
            - Total Portfolio Value: $125,450
            - Daily P&L: +$1,250.75 (+1.01%)
            - Top Performer: GOOGL (+6.7%)
            - Underperformer: MSFT (-2.1%)
            - Sector Allocation: 45% Technology, 20% Healthcare, 15% Financials, 20% Other
            - Risk Score: 6/10 (Moderate-High)
            """

            full_prompt = f"{portfolio_context}\n\n{insight_text}"

            with st.spinner("Generating portfolio insight..."):
                if voice_assistant.client:
                    try:
                        response = voice_assistant.client.chat.completions.create(
                            model="gpt-4",
                            messages=[
                                {"role": "system", "content": "You are Agent Chopra, a professional AI trading assistant. Provide clear, actionable insights in a conversational tone suitable for voice delivery. Keep responses under 150 words."},
                                {"role": "user", "content": full_prompt}
                            ],
                            max_tokens=200,
                            temperature=0.7
                        )

                        insight_content = response.choices[0].message.content

                        st.markdown("#### 📝 Portfolio Insight:")
                        st.info(insight_content)

                        # Generate audio
                        with st.spinner("Converting to speech..."):
                            audio_content = voice_assistant.text_to_speech(
                                insight_content,
                                voice=voice_type,
                                model=voice_model
                            )

                            if audio_content:
                                st.markdown("#### 🔊 Audio Insight:")
                                voice_assistant.create_audio_player(audio_content, autoplay=autoplay)

                    except Exception as e:
                        st.error(f"Error generating insight: {str(e)}")
                else:
                    st.error("OpenAI API not configured. Please add your API key to enable voice features.")

def create_voice_quick_actions():
    """Create quick voice actions for the sidebar"""
    st.sidebar.markdown("""
    <div style='background: linear-gradient(135deg, #1a1a1a 0%, #2d1b1b 100%);
                padding: 15px; border-radius: 10px; margin-bottom: 20px;
                border: 1px solid #DC143C;'>
        <h3 style='color: #DC143C; margin: 0; text-align: center;'>🎤 Quick Voice</h3>
    </div>
    """, unsafe_allow_html=True)

    voice_assistant = VoiceAssistant()

    quick_phrases = [
        "Market opening bell summary",
        "Portfolio status update",
        "Risk alert notification",
        "Trading day recap"
    ]

    selected_phrase = st.sidebar.selectbox("Quick voice update", quick_phrases)

    if st.sidebar.button("🗣️ Speak", type="primary"):
        phrase_content = {
            "Market opening bell summary": "Good morning! The market has opened with mixed sentiment. Tech stocks are showing strength while energy sectors face headwinds. Stay alert for volatility in the first hour of trading.",
            "Portfolio status update": "Your portfolio is currently up 1.2% for the day with strong performance from your technology holdings. GOOGL is leading gains while MSFT is showing some weakness.",
            "Risk alert notification": "Risk management alert: Your portfolio concentration in technology exceeds 45%. Consider diversifying into defensive sectors to reduce correlation risk.",
            "Trading day recap": "Trading day complete! Portfolio gained 0.8% with 3 winning positions and 1 loser. Tomorrow's focus: watch earnings reports and Fed commentary for direction."
        }

        content = phrase_content[selected_phrase]

        with st.sidebar:
            with st.spinner("Speaking..."):
                audio_content = voice_assistant.text_to_speech(content, voice="alloy")
                if audio_content:
                    voice_assistant.create_audio_player(audio_content, autoplay=True)

# Voice command processing (future enhancement)
def process_voice_commands():
    """Process voice commands for trading actions"""
    st.markdown("""
    <div style='background: #1a1a1a; padding: 15px; border-radius: 8px; margin-bottom: 20px;
                border: 2px dashed #DC143C;'>
        <h4 style='color: #DC143C; margin: 0; text-align: center;'>🎙️ Voice Commands (Coming Soon)</h4>
        <p style='color: #888; text-align: center; margin: 10px 0 0 0;'>
            Future feature: Voice-activated trading commands<br>
            "Agent Chopra, buy 100 shares of AAPL"<br>
            "What's my portfolio performance today?"<br>
            "Show me trending stocks in tech sector"
        </p>
    </div>
    """, unsafe_allow_html=True)