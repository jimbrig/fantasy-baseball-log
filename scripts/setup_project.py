#!/usr/bin/env python3
"""
setup_project.py - Set up the Fantasy Baseball Decision Log project

This script helps users set up the Fantasy Baseball Decision Log project by:
1. Creating the necessary directory structure
2. Setting up the .env file with Yahoo API credentials
3. Running the initial OAuth authentication
4. Collecting initial data
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import getpass

# Configuration
PROJECT_ROOT = Path('.')
REQUIRED_DIRS = [
    'data',
    'data/roster-snapshots',
    'data/player-stats',
    'data/category-performance',
    'data/analysis',
    'data/visualizations',
    'decisions',
    'decisions/draft',
    'decisions/waiver-moves',
    'decisions/trades',
    'decisions/lineups',
    'decisions/reviews',
    'templates',
    'scripts',
    'docs'
]


def create_directory_structure():
    """Create the necessary directory structure"""
    print("Creating directory structure...")
    
    for directory in REQUIRED_DIRS:
        dir_path = PROJECT_ROOT / directory
        dir_path.mkdir(exist_ok=True, parents=True)
        print(f"  Created {dir_path}")
    
    print("Directory structure created successfully.")
    return True


def setup_env_file():
    """Set up the .env file with Yahoo API credentials"""
    print("\nSetting up .env file with Yahoo API credentials...")
    
    env_path = PROJECT_ROOT / '.env'
    
    # Check if .env file already exists
    if env_path.exists():
        overwrite = input(".env file already exists. Overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            print("Skipping .env file setup.")
            return True
    
    # Get Yahoo API credentials
    print("\nYou'll need to create a Yahoo Developer App to get API credentials.")
    print("Visit https://developer.yahoo.com/apps/ to create an app.")
    print("Make sure to set the callback URL to https://localhost:8000/callback")
    
    client_id = input("\nEnter your Yahoo Client ID: ")
    client_secret = getpass.getpass("Enter your Yahoo Client Secret: ")
    redirect_uri = input("Enter your Callback Domain (default: https://localhost:8000/callback): ")
    
    if not redirect_uri:
        redirect_uri = "https://localhost:8000/callback"
    
    # Write to .env file
    with open(env_path, 'w') as f:
        f.write(f"YAHOO_CLIENT_ID={client_id}\n")
        f.write(f"YAHOO_CLIENT_SECRET={client_secret}\n")
        f.write(f"YAHOO_REDIRECT_URI={redirect_uri}\n")
    
    print(f".env file created at {env_path}")
    return True


def run_oauth_authentication():
    """Run the initial OAuth authentication"""
    print("\nRunning initial OAuth authentication...")
    
    oauth_script = PROJECT_ROOT / 'scripts' / 'yahoo_oauth.experimental.py'
    
    if not oauth_script.exists():
        print(f"Error: OAuth script not found at {oauth_script}")
        return False
    
    try:
        # Run the OAuth script
        subprocess.run(['python', str(oauth_script)], check=True)
        
        # Check if oauth2.json was created
        oauth_file = PROJECT_ROOT / 'oauth2.json'
        if oauth_file.exists():
            print("OAuth authentication completed successfully.")
            return True
        else:
            print("Error: OAuth authentication failed. oauth2.json not created.")
            return False
    
    except subprocess.CalledProcessError as e:
        print(f"Error running OAuth authentication: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def collect_initial_data():
    """Collect initial data from Yahoo Fantasy API"""
    print("\nCollecting initial data from Yahoo Fantasy API...")
    
    data_script = PROJECT_ROOT / 'scripts' / 'daily_data_collection.py'
    
    if not data_script.exists():
        print(f"Error: Data collection script not found at {data_script}")
        return False
    
    try:
        # Run the data collection script
        subprocess.run(['python', str(data_script)], check=True)
        
        # Check if data was collected
        today = Path('data') / Path(os.popen('date +%Y-%m-%d').read().strip())
        if today.exists() and any(today.iterdir()):
            print("Initial data collection completed successfully.")
            return True
        else:
            print("Warning: Data collection may have failed. No data files found.")
            return False
    
    except subprocess.CalledProcessError as e:
        print(f"Error collecting initial data: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def install_dependencies():
    """Install required Python dependencies"""
    print("\nInstalling required Python dependencies...")
    
    requirements_file = PROJECT_ROOT / 'requirements.txt'
    
    if not requirements_file.exists():
        print(f"Error: requirements.txt not found at {requirements_file}")
        return False
    
    try:
        # Install dependencies
        subprocess.run(['pip', 'install', '-r', str(requirements_file)], check=True)
        print("Dependencies installed successfully.")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def main():
    """Main function to set up the project"""
    print("Setting up Fantasy Baseball Decision Log project...\n")
    
    # Create directory structure
    if not create_directory_structure():
        print("Error creating directory structure. Aborting setup.")
        return 1
    
    # Install dependencies
    if not install_dependencies():
        print("Error installing dependencies. Aborting setup.")
        return 1
    
    # Set up .env file
    if not setup_env_file():
        print("Error setting up .env file. Aborting setup.")
        return 1
    
    # Run OAuth authentication
    if not run_oauth_authentication():
        print("Error running OAuth authentication. Aborting setup.")
        return 1
    
    # Collect initial data
    if not collect_initial_data():
        print("Warning: Initial data collection may have failed.")
    
    print("\nFantasy Baseball Decision Log project setup completed successfully!")
    print("\nNext steps:")
    print("1. Create a draft analysis using: python scripts/create_decision_log.py draft")
    print("2. Run category analysis using: python scripts/run_analysis.py category")
    print("3. Find waiver opportunities using: python scripts/run_analysis.py waiver")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
