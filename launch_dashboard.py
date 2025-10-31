#!/usr/bin/env python3
"""
Dashboard Launcher
Quick launcher for the Streamlit trading dashboard
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'plotly',
        'streamlit-autorefresh',
        'alpaca-py',
        'python-dotenv',
        'pandas'
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)

def launch_dashboard():
    """Launch the Streamlit dashboard"""
    script_dir = Path(__file__).parent
    dashboard_path = script_dir / "trading_dashboard.py"

    print("="*60)
    print(" LAUNCHING ALPACA TRADING DASHBOARD ".center(60))
    print("="*60)
    print(f"Dashboard URL will open in your browser...")
    print(f"Dashboard file: {dashboard_path}")
    print("="*60)

    try:
        # Launch Streamlit
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run',
            str(dashboard_path),
            '--server.port=8501',
            '--server.address=localhost',
            '--server.headless=false',
            '--browser.gatherUsageStats=false'
        ])
    except KeyboardInterrupt:
        print("\nDashboard stopped by user")
    except Exception as e:
        print(f"Error launching dashboard: {e}")

if __name__ == "__main__":
    # Change to script directory
    os.chdir(Path(__file__).parent)

    # Check and install dependencies
    check_dependencies()

    # Launch dashboard
    launch_dashboard()