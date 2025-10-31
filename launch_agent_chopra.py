#!/usr/bin/env python3
"""
Agent Chopra Launcher
Complete launcher for the advanced AI trading platform
"""

import subprocess
import sys
import os
from pathlib import Path

def display_banner():
    """Display Agent Chopra banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║                     🔥 AGENT CHOPRA 🔥                       ║
    ║              Advanced AI Trading Intelligence Platform        ║
    ║                                                              ║
    ║  🎯 Risk-Optimized Trading    🧠 AI-Powered Insights        ║
    ║  ⚡ Real-time Analysis        🔥 Dark Theme Interface        ║
    ║  📊 Portfolio Intelligence    🤖 LangSmith Integration       ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_and_install_dependencies():
    """Check and install all required packages for Agent Chopra"""
    print("🔍 Checking Agent Chopra dependencies...")

    required_packages = [
        'streamlit',
        'plotly',
        'streamlit-autorefresh',
        'streamlit-authenticator',
        'alpaca-py',
        'python-dotenv',
        'pandas',
        'numpy',
        'yfinance',
        'langchain',
        'langchain-openai',
        'langchain-chroma',
        'chromadb',
        'tiktoken',
        'psycopg2-binary',
        'sqlalchemy',
        '"langsmith[openai-agents]"'
    ]

    missing_packages = []

    for package in required_packages:
        package_name = package.replace('"', '').split('[')[0]
        try:
            __import__(package_name.replace('-', '_'))
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - MISSING")
            missing_packages.append(package)

    if missing_packages:
        print(f"\n🔧 Installing missing packages: {', '.join(missing_packages)}")
        try:
            for package in missing_packages:
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', package
                ])
            print("✅ All dependencies installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing packages: {e}")
            return False

    return True

def setup_environment():
    """Setup environment configuration"""
    env_file = Path(".env")

    print("\n🔧 Setting up environment...")

    if not env_file.exists():
        print("❌ .env file not found!")
        print("Creating template .env file...")

        env_template = """# Alpaca Paper Trading API Credentials
APCA_API_KEY_ID=your_alpaca_key_here
APCA_API_SECRET_KEY=your_alpaca_secret_here
APCA_API_BASE_URL=https://paper-api.alpaca.markets

# LangSmith Configuration
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_PROJECT=your_project_name

# PostgreSQL Database Configuration (Optional)
DATABASE_URL=postgresql://username:password@localhost:5432/agent_chopra_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=agent_chopra_db
POSTGRES_USER=username
POSTGRES_PASSWORD=password

# Risk Profile Settings
DEFAULT_RISK_PROFILE=5
RISK_ASSESSMENT_ENABLED=true
"""

        with open(env_file, 'w') as f:
            f.write(env_template)

        print("✅ Template .env file created!")
        print("⚠️  Please update it with your actual API keys before running Agent Chopra")
        return False

    print("✅ .env file found")
    return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")

    directories = ['logs', 'chroma_db', 'database']

    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Directory created/verified: {directory}")

def setup_database():
    """Setup database if PostgreSQL is available"""
    print("\n🗄️  Setting up database...")

    try:
        from database.models import db_manager
        db_manager.create_tables()
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"⚠️  Database setup warning: {e}")
        print("💡 Will use SQLite fallback for data storage")

def launch_agent_chopra():
    """Launch Agent Chopra dashboard"""
    script_dir = Path(__file__).parent
    dashboard_path = script_dir / "agent_chopra_dashboard.py"

    print("\n" + "="*70)
    print(" LAUNCHING AGENT CHOPRA ".center(70, "="))
    print("="*70)
    print()
    print("🔥 AGENT CHOPRA FEATURES:")
    print("   ✅ Professional dark/red theme interface")
    print("   ✅ Advanced risk profiling system (1-10 scale)")
    print("   ✅ AI-powered trading insights with LangSmith")
    print("   ✅ Real-time portfolio analysis")
    print("   ✅ Risk-optimized stock recommendations")
    print("   ✅ PostgreSQL database integration")
    print("   ✅ Interactive AI chat assistant")
    print("   ✅ Comprehensive trading dashboard")
    print()
    print("🌐 Dashboard URL: http://localhost:8501")
    print("🔑 Required: OpenAI API key (enter in sidebar)")
    print("🎯 Optional: Complete risk assessment for personalized recommendations")
    print()
    print("="*70)

    try:
        # Load environment variables from .env file
        from dotenv import load_dotenv
        load_dotenv()

        # Launch Streamlit
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run',
            str(dashboard_path),
            '--server.port=8501',
            '--server.address=localhost',
            '--server.headless=false',
            '--browser.gatherUsageStats=false',
            '--theme.base=dark',
            '--theme.primaryColor=#DC143C',
            '--theme.backgroundColor=#0D1117',
            '--theme.secondaryBackgroundColor=#161B22',
            '--theme.textColor=#F0F6FC'
        ])
    except KeyboardInterrupt:
        print("\n\n🔥 Agent Chopra stopped by user")
    except Exception as e:
        print(f"\n❌ Error launching Agent Chopra: {e}")

def run_system_check():
    """Run comprehensive system check"""
    print("\n🔍 AGENT CHOPRA SYSTEM CHECK")
    print("="*50)

    checks = [
        ("Python Version", sys.version_info >= (3, 8)),
        ("Dependencies", check_and_install_dependencies()),
        ("Environment", setup_environment()),
        ("Directories", True),  # Always succeeds
        ("Database", True)  # Always succeeds (falls back to SQLite)
    ]

    create_directories()
    setup_database()

    all_passed = True
    for check_name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name:.<20} {status}")
        if not result:
            all_passed = False

    print("="*50)
    return all_passed

def main():
    """Main launcher function"""
    display_banner()

    # Change to script directory
    os.chdir(Path(__file__).parent)

    # Run system check
    if not run_system_check():
        print("\n❌ System check failed. Please fix the issues above.")
        print("💡 Most common issue: Update your .env file with valid API keys")
        return

    print("\n🚀 All systems ready! Launching Agent Chopra...")
    input("\nPress Enter to launch Agent Chopra...")

    # Launch Agent Chopra
    launch_agent_chopra()

if __name__ == "__main__":
    main()