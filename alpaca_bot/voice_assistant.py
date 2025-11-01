#!/usr/bin/env python3
"""
Voice Assistant Module for Agent Chopra
Enhanced with Text-to-Speech capabilities
"""

import streamlit as st
import base64
import io

# Try to import text-to-speech libraries
try:
    import pyttsx3
    TTS_PYTTSX3_AVAILABLE = True
except ImportError:
    TTS_PYTTSX3_AVAILABLE = False

try:
    import openai
    OPENAI_TTS_AVAILABLE = True
except ImportError:
    OPENAI_TTS_AVAILABLE = False

class VoiceAssistant:
    """Enhanced voice assistant with TTS capabilities"""

    def __init__(self):
        self.enabled = False
        self.tts_engine = None
        self.openai_client = None
        self.init_tts()

    def init_tts(self):
        """Initialize text-to-speech engines"""
        # Try to initialize pyttsx3
        if TTS_PYTTSX3_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                # Configure voice properties
                self.tts_engine.setProperty('rate', 150)  # Speed of speech
                self.tts_engine.setProperty('volume', 0.8)  # Volume level
            except Exception as e:
                st.warning(f"pyttsx3 TTS initialization failed: {str(e)}")

        # Initialize OpenAI TTS if available
        if OPENAI_TTS_AVAILABLE and st.session_state.get('openai_api_key'):
            try:
                self.openai_client = openai.OpenAI(api_key=st.session_state.openai_api_key)
            except Exception as e:
                st.warning(f"OpenAI TTS initialization failed: {str(e)}")

    def speak_text_pyttsx3(self, text: str):
        """Speak text using pyttsx3 (local TTS)"""
        if not self.tts_engine:
            return False

        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            return True
        except Exception as e:
            st.error(f"pyttsx3 TTS error: {str(e)}")
            return False

    def speak_text_openai(self, text: str):
        """Generate speech using OpenAI TTS and return audio for browser playback"""
        if not self.openai_client:
            return None

        try:
            response = self.openai_client.audio.speech.create(
                model="tts-1",
                voice="alloy",  # You can change this to other voices: echo, fable, onyx, nova, shimmer
                input=text[:4000]  # Limit text length
            )

            # Convert to base64 for HTML audio player
            audio_data = response.content
            audio_base64 = base64.b64encode(audio_data).decode()

            return audio_base64
        except Exception as e:
            st.error(f"OpenAI TTS error: {str(e)}")
            return None

    def create_audio_player(self, audio_base64: str):
        """Create HTML audio player for browser playback"""
        audio_html = f"""
        <audio controls autoplay style="width: 100%;">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)

    def speak_text(self, text: str, method: str = "auto"):
        """Main TTS function with multiple methods"""
        if not text.strip():
            return False

        # Clean text for TTS
        clean_text = text.replace("*", "").replace("#", "").replace("`", "")

        if method == "openai" or (method == "auto" and self.openai_client):
            # Use OpenAI TTS (higher quality, requires API)
            audio_base64 = self.speak_text_openai(clean_text)
            if audio_base64:
                self.create_audio_player(audio_base64)
                return True

        if method == "local" or (method == "auto" and self.tts_engine):
            # Use local TTS (no API required but lower quality)
            return self.speak_text_pyttsx3(clean_text)

        st.warning("⚠️ No TTS engine available. Please configure OpenAI API key or install pyttsx3.")
        return False

    def process_command(self, command):
        """Process voice command"""
        return f"Voice command received: {command}"

def create_voice_interface():
    """Create enhanced voice interface with TTS"""
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1a1a1a 0%, #2d1b1b 100%);
                padding: 20px; border-radius: 15px; margin-bottom: 20px;
                border: 2px solid #DC143C;'>
        <h2 style='color: #DC143C; margin: 0; text-align: center;'>
            🎤 VOICE ASSISTANT
        </h2>
        <p style='color: #888; text-align: center; margin: 5px 0 0 0;'>
            Enhanced with Text-to-Speech capabilities
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize voice assistant
    if 'voice_assistant' not in st.session_state:
        st.session_state.voice_assistant = VoiceAssistant()

    voice_assistant = st.session_state.voice_assistant

    # TTS Demo Section
    st.markdown("### 🔊 Text-to-Speech Demo")

    col1, col2 = st.columns([3, 1])

    with col1:
        text_to_speak = st.text_area(
            "Enter text to convert to speech:",
            value="Welcome to Agent Chopra! Your AI-powered trading assistant is ready to help you make informed investment decisions.",
            height=100
        )

    with col2:
        st.markdown("**TTS Method:**")
        tts_method = st.radio(
            "Select TTS Engine:",
            ["Auto", "OpenAI (High Quality)", "Local (pyttsx3)"],
            key="tts_method"
        )

        method_map = {
            "Auto": "auto",
            "OpenAI (High Quality)": "openai",
            "Local (pyttsx3)": "local"
        }

    # TTS Controls
    col3, col4, col5 = st.columns(3)

    with col3:
        if st.button("🔊 Speak Text", type="primary", use_container_width=True):
            if text_to_speak.strip():
                with st.spinner("Generating speech..."):
                    success = voice_assistant.speak_text(text_to_speak, method_map[tts_method])
                    if success:
                        st.success("✅ Speech generated successfully!")
                    else:
                        st.error("❌ Failed to generate speech")
            else:
                st.warning("⚠️ Please enter some text to speak")

    with col4:
        if st.button("📊 Market Summary", use_container_width=True):
            market_summary = """
            Good day, trader! Here's your market summary: The S&P 500 is showing positive momentum today.
            Technology stocks are leading gains, while defensive sectors remain stable.
            Agent Chopra recommends reviewing your risk allocation based on current market conditions.
            """
            with st.spinner("Generating market summary..."):
                voice_assistant.speak_text(market_summary, method_map[tts_method])

    with col5:
        if st.button("🎯 AI Insights", use_container_width=True):
            ai_insights = """
            Based on your risk profile, Agent Chopra suggests focusing on diversified portfolio allocation.
            Current market sentiment shows moderate optimism. Consider maintaining your current positions
            while monitoring key economic indicators for potential opportunities.
            """
            with st.spinner("Generating AI insights..."):
                voice_assistant.speak_text(ai_insights, method_map[tts_method])

    # TTS Status and Configuration
    st.markdown("---")
    st.markdown("### ⚙️ TTS Configuration")

    status_cols = st.columns(3)

    with status_cols[0]:
        openai_status = "✅ Available" if voice_assistant.openai_client else "❌ Not Available"
        st.metric("OpenAI TTS", openai_status)

    with status_cols[1]:
        local_status = "✅ Available" if voice_assistant.tts_engine else "❌ Not Available"
        st.metric("Local TTS (pyttsx3)", local_status)

    with status_cols[2]:
        api_status = "✅ Configured" if st.session_state.get('openai_api_key') else "❌ Not Set"
        st.metric("OpenAI API Key", api_status)

    # Installation Instructions
    if not voice_assistant.tts_engine and not voice_assistant.openai_client:
        st.markdown("### 📦 Setup Instructions")
        st.info("""
        **To enable Text-to-Speech:**

        **Option 1: OpenAI TTS (Recommended - High Quality)**
        - Add your OpenAI API key in the sidebar
        - No additional installation required

        **Option 2: Local TTS (Free but Basic Quality)**
        - Install pyttsx3: `pip install pyttsx3`
        - Works offline, no API key required
        """)

def create_voice_quick_actions():
    """Create voice quick actions"""
    st.subheader("🎤 Voice Quick Actions")

    if 'voice_assistant' not in st.session_state:
        st.session_state.voice_assistant = VoiceAssistant()

    voice_assistant = st.session_state.voice_assistant

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🎯 Portfolio Status", use_container_width=True):
            portfolio_status = "Your portfolio is performing well today. Overall gains of 2.3 percent. Technology holdings are leading with strong performance."
            voice_assistant.speak_text(portfolio_status)

    with col2:
        if st.button("📈 Market Update", use_container_width=True):
            market_update = "Market update: The Dow Jones is up 150 points. NASDAQ showing strength in tech sector. Oil prices stable at current levels."
            voice_assistant.speak_text(market_update)

    with col3:
        if st.button("⚠️ Risk Alert", use_container_width=True):
            risk_alert = "Risk assessment: Your current allocation aligns with your moderate risk profile. No immediate action required."
            voice_assistant.speak_text(risk_alert)