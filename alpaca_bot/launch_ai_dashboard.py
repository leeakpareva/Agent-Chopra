#!/usr/bin/env python3
"""
AI-Enhanced Dashboard Launcher
Launches the enhanced trading dashboard with AI capabilities
"""

import subprocess
import sys
import os
from pathlib import Path

def check_and_install_dependencies():
    """Check and install all required packages"""
    required_packages = [
        'streamlit',
        'plotly',
        'streamlit-autorefresh',
        'alpaca-py',
        'python-dotenv',
        'pandas',
        'langchain',
        'langchain-openai',
        'langchain-chroma',
        'chromadb',
        'tiktoken'
    ]

    print("Checking dependencies...")
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)

    if missing_packages:
        print(f"\nInstalling missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install'
            ] + missing_packages)
            print("✅ All dependencies installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing packages: {e}")
            return False

    return True

def check_environment():
    """Check environment configuration"""
    env_file = Path(".env")

    if not env_file.exists():
        print("❌ .env file not found!")
        print("Please create a .env file with your Alpaca API credentials:")
        print("""
        APCA_API_KEY_ID=your_api_key_here
        APCA_API_SECRET_KEY=your_secret_key_here
        APCA_API_BASE_URL=https://paper-api.alpaca.markets
        """)
        return False

    print("✅ .env file found")
    return True

def create_directories():
    """Create necessary directories"""
    directories = ['logs', 'chroma_db']

    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Directory created/verified: {directory}")

def launch_enhanced_dashboard():
    """Launch the enhanced Streamlit dashboard"""
    script_dir = Path(__file__).parent
    dashboard_path = script_dir / "enhanced_dashboard.py"

    print("="*70)
    print(" LAUNCHING AI-ENHANCED TRADING DASHBOARD ".center(70))
    print("="*70)
    print()
    print("🚀 Features enabled:")
    print("   ✅ Real-time trading interface")
    print("   ✅ Portfolio visualization")
    print("   ✅ Order management")
    print("   ✅ AI-powered insights")
    print("   ✅ Intelligent chat assistant")
    print("   ✅ Portfolio analysis")
    print("   ✅ Trading recommendations")
    print()
    print("🌐 Dashboard will open in your browser...")
    print("🔗 URL: http://localhost:8501")
    print()
    print("💡 Don't forget to enter your OpenAI API key in the sidebar")
    print("   to unlock AI features!")
    print()
    print("="*70)

    try:
        # Launch Streamlit
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run',
            str(dashboard_path),
            '--server.port=8501',
            '--server.address=localhost',
            '--server.headless=false',
            '--browser.gatherUsageStats=false',
            '--theme.base=light',
            '--theme.primaryColor=#667eea'
        ])
    except KeyboardInterrupt:
        print("\n\n⏹️ Dashboard stopped by user")
    except Exception as e:
        print(f"\n❌ Error launching dashboard: {e}")

def main():
    """Main launcher function"""
    print("🚀 AI-Enhanced Trading Dashboard Launcher")
    print("=" * 50)

    # Change to script directory
    os.chdir(Path(__file__).parent)

    # Check and install dependencies
    if not check_and_install_dependencies():
        print("❌ Dependency installation failed. Please check your Python environment.")
        return

    # Check environment
    if not check_environment():
        print("❌ Environment check failed. Please configure your .env file.")
        return

    # Create directories
    create_directories()

    # Launch dashboard
    launch_enhanced_dashboard()

if __name__ == "__main__":
    main()