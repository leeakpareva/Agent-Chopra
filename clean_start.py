#!/usr/bin/env python3
"""
Clean Start Script for Agent Chopra
Kills any existing processes and starts fresh
"""

import subprocess
import sys
import os
import signal
import time
from pathlib import Path

def kill_existing_processes():
    """Kill any existing Streamlit/Python processes"""
    try:
        # Kill by port
        subprocess.run([
            'cmd', '/c', 'for /f "tokens=5" %a in (\'netstat -aon ^| findstr :8501\') do taskkill /f /pid %a'
        ], shell=True, capture_output=True)

        # Kill any streamlit processes
        subprocess.run(['taskkill', '/f', '/im', 'streamlit.exe'], capture_output=True)

        # Kill python processes that might be streamlit
        result = subprocess.run(['tasklist', '/fi', 'imagename eq python3.11.exe'],
                              capture_output=True, text=True)

        if 'python3.11.exe' in result.stdout:
            # More aggressive cleanup
            subprocess.run(['taskkill', '/f', '/im', 'python3.11.exe'], capture_output=True)

        print("Cleaned up existing processes")
        time.sleep(2)  # Wait for cleanup

    except Exception as e:
        print(f"Cleanup warning: {e}")

def verify_files():
    """Verify all Agent Chopra files are present"""
    required_files = [
        'agent_chopra_dashboard.py',
        'launch_agent_chopra.py',
        'ai_trading_assistant.py',
        'risk_profiler.py',
        'trading_dashboard.py',
        'database/models.py',
        '.env',
        'requirements_agent_chopra.txt'
    ]

    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)

    if missing_files:
        print(f"Missing files: {missing_files}")
        return False

    print("All Agent Chopra files verified")
    return True

def start_agent_chopra():
    """Start Agent Chopra with clean environment"""
    try:
        # Load environment variables from .env file
        from dotenv import load_dotenv
        load_dotenv()

        print("Starting Agent Chopra...")
        print("Will open at: http://localhost:8501")
        print("If port 8501 is still busy, will try port 8502")

        # Try port 8501 first, then 8502 if busy
        for port in [8501, 8502]:
            try:
                subprocess.run([
                    sys.executable, '-m', 'streamlit', 'run',
                    'agent_chopra_dashboard.py',
                    f'--server.port={port}',
                    '--server.address=localhost',
                    '--server.headless=false',
                    '--browser.gatherUsageStats=false',
                    '--theme.base=dark',
                    '--theme.primaryColor=#DC143C',
                    '--theme.backgroundColor=#0D1117',
                    '--theme.secondaryBackgroundColor=#161B22',
                    '--theme.textColor=#F0F6FC'
                ], check=True)
                break
            except subprocess.CalledProcessError:
                if port == 8501:
                    print(f"Port 8501 busy, trying 8502...")
                    continue
                else:
                    raise

    except KeyboardInterrupt:
        print("\nAgent Chopra stopped by user")
    except Exception as e:
        print(f"Error starting Agent Chopra: {e}")

def main():
    """Main function"""
    print("AGENT CHOPRA - CLEAN START")
    print("="*50)

    # Change to script directory
    os.chdir(Path(__file__).parent)

    # Kill existing processes
    print("Cleaning up existing processes...")
    kill_existing_processes()

    # Verify files
    print("Verifying files...")
    if not verify_files():
        print("File verification failed")
        return

    # Start Agent Chopra
    start_agent_chopra()

if __name__ == "__main__":
    main()