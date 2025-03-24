#!/usr/bin/env python3
"""
daily_data_collection.py - Daily data collection script for fantasy baseball

This script fetches data from the Yahoo Fantasy API and saves it to the data directory.
It's designed to be run daily to collect historical data for analysis.
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
import yahoo_fantasy_api as yfa
from yahoo_oauth import OAuth2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
DATA_DIR = Path('./data')


def connect_to_yahoo_api():
    """Connect to Yahoo Fantasy API"""
    print("Connecting to Yahoo Fantasy API...")
    
    try:
        # Check if oauth2.json exists
        if not os.path.exists('oauth2.json'):
            print("OAuth2 credentials file not found. Please run yahoo_oauth.py first.")
            return None
        
        # Initialize OAuth session
        oauth = OAuth2(None, None, from_file='oauth2.json')
        
        # Check if token is valid
        if not oauth.token_is_valid():
            print("OAuth token needs refreshing...")
            oauth.refresh_access_token()
        
        print("Successfully connected to Yahoo Fantasy API")
        return oauth
    
    except Exception as e:
        print(f"Error connecting to Yahoo Fantasy API: {e}")
        return None


def get_league_data(oauth):
    """Get league data from Yahoo Fantasy API"""
    print("Fetching league data...")
    
    try:
        # Access your game
        gm = yfa.game.Game(oauth, 'mlb')
        
        # Get your league IDs (adjust year as needed)
        league_ids = gm.league_ids(year=2025)
        
        if not league_ids:
            print("No leagues found for 2025.")
            return None
        
        # Use the first league ID
        lg = gm.to_league(league_ids[0])
        print(f"Using league ID: {lg.league_id}")
        
        return lg
    
    except Exception as e:
        print(f"Error fetching league data: {e}")
        return None


def fetch_and_save_data(lg):
    """Fetch data from Yahoo Fantasy API and save it to the data directory"""
    print("Fetching and saving data...")
    
    try:
        # Create date directory
        today = datetime.today().strftime('%Y-%m-%d')
        data_dir = DATA_DIR / today
        data_dir.mkdir(exist_ok=True, parents=True)
        
        # Fetch teams data
        teams = lg.teams()
        teams_file = data_dir / 'teams.json'
        with open(teams_file, 'w') as f:
            json.dump(teams, f, indent=4)
        print(f"Saved teams data to {teams_file}")
        
        # Fetch standings data
        standings = lg.standings()
        standings_file = data_dir / 'standings.json'
        with open(standings_file, 'w') as f:
            json.dump(standings, f, indent=4)
        print(f"Saved standings data to {standings_file}")
        
        # Fetch draft results data
        draft_results = lg.draft_results()
        draft_results_file = data_dir / 'draft_results.json'
        with open(draft_results_file, 'w') as f:
            json.dump(draft_results, f, indent=4)
        print(f"Saved draft results data to {draft_results_file}")
        
        # Fetch roster data for each team
        rosters = {}
        for team_id, team_data in teams.items():
            try:
                team = lg.to_team(team_id)
                roster = team.roster()
                rosters[team_id] = roster
                time.sleep(1)  # Avoid rate limiting
            except Exception as e:
                print(f"Error fetching roster for team {team_id}: {e}")
        
        rosters_file = data_dir / 'rosters.json'
        with open(rosters_file, 'w') as f:
            json.dump(rosters, f, indent=4)
        print(f"Saved rosters data to {rosters_file}")
        
        # Fetch league settings
        settings = lg.settings()
        settings_file = data_dir / 'settings.json'
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=4)
        print(f"Saved league settings to {settings_file}")
        
        # Create a combined data file
        combined_data = {
            'date': today,
            'teams': teams,
            'standings': standings,
            'draft_results': draft_results,
            'rosters': rosters,
            'settings': settings
        }
        
        combined_file = data_dir / 'combined_data.json'
        with open(combined_file, 'w') as f:
            json.dump(combined_data, f, indent=4)
        print(f"Saved combined data to {combined_file}")
        
        # Also save to roster-snapshots directory
        roster_snapshots_dir = DATA_DIR / 'roster-snapshots'
        roster_snapshots_dir.mkdir(exist_ok=True, parents=True)
        roster_snapshot_file = roster_snapshots_dir / f'{today}.json'
        with open(roster_snapshot_file, 'w') as f:
            json.dump(rosters, f, indent=4)
        print(f"Saved roster snapshot to {roster_snapshot_file}")
        
        return True
    
    except Exception as e:
        print(f"Error fetching and saving data: {e}")
        return False


def main():
    """Main function to run the daily data collection"""
    print(f"Starting daily data collection at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Connect to Yahoo API
    oauth = connect_to_yahoo_api()
    if not oauth:
        return False
    
    # Get league data
    lg = get_league_data(oauth)
    if not lg:
        return False
    
    # Fetch and save data
    success = fetch_and_save_data(lg)
    
    if success:
        print(f"Daily data collection completed successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print(f"Daily data collection failed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return success


if __name__ == "__main__":
    main()
