"""
Yahoo Fantasy API service
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yahoo_fantasy_api as yfa
from yahoo_oauth import OAuth2

from app.core.config import settings

logger = logging.getLogger(__name__)


class YahooFantasyService:
    """Service for interacting with Yahoo Fantasy API"""

    def __init__(self):
        self.oauth = None
        self.game = None
        self.league = None
        self.oauth_file = "oauth2.json"

    def initialize(self) -> bool:
        """Initialize the Yahoo Fantasy API connection"""
        try:
            # Check if credentials are set
            client_id = os.getenv("YAHOO_CLIENT_ID") or settings.YAHOO_CLIENT_ID
            client_secret = os.getenv("YAHOO_CLIENT_SECRET") or settings.YAHOO_CLIENT_SECRET

            if not client_id or not client_secret:
                logger.error("Yahoo API credentials not set")
                return False

            # Check if oauth2.json exists
            oauth2_file_exists = os.path.exists(self.oauth_file)

            if not oauth2_file_exists:
                # Create credentials file with minimal info needed for initial auth
                creds = {
                    "consumer_key": client_id,
                    "consumer_secret": client_secret
                }

                with open(self.oauth_file, "w") as f:
                    f.write(json.dumps(creds))

            # Initialize OAuth session
            self.oauth = OAuth2(None, None, from_file=self.oauth_file)

            # Check if token is valid or can be refreshed
            if not self.oauth.token_is_valid():
                logger.info("OAuth token needs refreshing")
                if not self.oauth.refresh_access_token():
                    logger.error("Failed to refresh OAuth token")
                    return False

            # Initialize game
            self.game = yfa.game.Game(self.oauth, 'mlb')

            # Get league IDs for current year
            current_year = datetime.now().year
            league_ids = self.game.league_ids(year=current_year)

            if not league_ids:
                logger.warning(f"No leagues found for {current_year}")
                return False

            # Use the first league
            self.league = self.game.to_league(league_ids[0])
            logger.info(f"Initialized Yahoo Fantasy API with league ID: {self.league.league_id}")

            return True

        except Exception as e:
            logger.error(f"Error initializing Yahoo Fantasy API: {e}")
            return False

    def get_teams(self) -> Dict[str, Any]:
        """Get all teams in the league"""
        if not self.league:
            logger.error("League not initialized")
            return {}

        try:
            return self.league.teams()
        except Exception as e:
            logger.error(f"Error getting teams: {e}")
            return {}

    def get_standings(self) -> List[Dict[str, Any]]:
        """Get current standings"""
        if not self.league:
            logger.error("League not initialized")
            return []

        try:
            return self.league.standings()
        except Exception as e:
            logger.error(f"Error getting standings: {e}")
            return []

    def get_draft_results(self) -> List[Dict[str, Any]]:
        """Get draft results"""
        if not self.league:
            logger.error("League not initialized")
            return []

        try:
            return self.league.draft_results()
        except Exception as e:
            logger.error(f"Error getting draft results: {e}")
            return []

    def get_roster(self, team_key: str) -> List[Dict[str, Any]]:
        """Get roster for a team"""
        if not self.league:
            logger.error("League not initialized")
            return []

        try:
            team = self.league.to_team(team_key)
            return team.roster()
        except Exception as e:
            logger.error(f"Error getting roster for team {team_key}: {e}")
            return []

    def get_league_settings(self) -> Dict[str, Any]:
        """Get league settings"""
        if not self.league:
            logger.error("League not initialized")
            return {}

        try:
            return self.league.settings()
        except Exception as e:
            logger.error(f"Error getting league settings: {e}")
            return {}

    def collect_data(self) -> Dict[str, Any]:
        """Collect all data from Yahoo Fantasy API"""
        if not self.league:
            logger.error("League not initialized")
            return {}

        try:
            # Get current date
            today = datetime.today().strftime('%Y-%m-%d')

            # Get teams
            teams = self.get_teams()

            # Get standings
            standings = self.get_standings()

            # Get draft results
            draft_results = self.get_draft_results()

            # Get rosters for each team
            rosters = {}
            for team_id in teams:
                rosters[team_id] = self.get_roster(team_id)

            # Get league settings
            settings = self.get_league_settings()

            # Combine all data
            combined_data = {
                "date": today,
                "teams": teams,
                "standings": standings,
                "draft_results": draft_results,
                "rosters": rosters,
                "settings": settings
            }

            return combined_data

        except Exception as e:
            logger.error(f"Error collecting data: {e}")
            return {}

    def save_data_to_json(self, data: Dict[str, Any], filename: str) -> bool:
        """Save data to JSON file"""
        try:
            # Create date directory
            today = datetime.today().strftime('%Y-%m-%d')
            data_dir = settings.JSON_DATA_DIR / today
            data_dir.mkdir(exist_ok=True, parents=True)

            # Save file
            file_path = data_dir / filename
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)

            logger.info(f"Saved data to {file_path}")
            return True

        except Exception as e:
            logger.error(f"Error saving data to {filename}: {e}")
            return False


# Create a singleton instance
yahoo_service = YahooFantasyService()
