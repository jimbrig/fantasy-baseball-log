import yahoo_fantasy_api as yfa
from yahoo_oauth import OAuth2
from dotenv import load_dotenv
import json
import os
import time

# Load environment variables from .env file
load_dotenv()

# Get environment variables with credentials
client_id = os.getenv('YAHOO_CLIENT_ID')
client_secret = os.getenv('YAHOO_CLIENT_SECRET')
redirect_uri = os.getenv('YAHOO_REDIRECT_URI')

# Check if oauth2.json exists and contains valid token information
oauth2_file_exists = os.path.exists('oauth2.json')
oauth = None

print(f"Checking for existing oauth2.json file: {'Found' if oauth2_file_exists else 'Not found'}")

if oauth2_file_exists:
    try:
        # Try to load existing OAuth2 token
        print("Loading existing OAuth token...")
        oauth = OAuth2(None, None, from_file='oauth2.json')
        
        # Check if the token is valid or can be refreshed
        if oauth.token_is_valid():
            print("Existing token is valid, using it")
        elif oauth.refresh_access_token():
            print("Existing token refreshed successfully")
        else:
            print("Existing token can't be refreshed, will create new one")
            oauth = None
    except Exception as e:
        print(f"Error loading existing OAuth token: {e}")
        oauth = None

# If we don't have a valid OAuth object, create a new one
if oauth is None:
    print("Creating new OAuth token (will require verification)")
    # Create credentials file with minimal info needed for initial auth
    creds = {
        'consumer_key': client_id,
        'consumer_secret': client_secret
    }
    
    with open('oauth2.json', "w") as f:
        f.write(json.dumps(creds))
    
    # Initialize new OAuth session
    oauth = OAuth2(None, None, from_file='oauth2.json')
    print("New OAuth token created and saved")

# Refresh token if needed
if not oauth.token_is_valid():
    print("Token needs refreshing")
    oauth.refresh_access_token()
    print("Token refreshed")
else:
    print("Token is valid, no refresh needed")

# Access your game (for baseball)
gm = yfa.game.Game(oauth, 'mlb')
print('Game ID:', gm.game_id)
# Game ID: <bound method Game.game_id of <yahoo_fantasy_api.game.Game object at 0x00000220E5FF6120>>

# Get your league IDs (adjust year as needed for 2025)
league_ids = gm.league_ids(year=2025)
lg = gm.to_league(league_ids[0])  # Use the first league ID
print('League ID:', lg.league_id)
# League ID: 458.l.56606

# Now you can access league data
teams = lg.teams()
# print('Teams:', teams)

standings = lg.standings()
# print('Standings:', standings)

draft_results = lg.draft_results()
# print('Draft Results:', draft_results)

# collect data for export
data = {
    'league_id': lg.league_id,
    'teams': json.dumps(teams),
    'standings': json.dumps(standings),
    'draft_results': json.dumps(draft_results),
}

# save all data to json file
def save_to_json(data, filename):
    import json
    import os
    from datetime import datetime
    
    data_dir = './data/'

    # get today's date
    today = datetime.today().strftime('%Y-%m-%d')

    # create date directory
    data_dir = os.path.join(data_dir, today)
    os.makedirs(data_dir, exist_ok=True)

    with open(os.path.join(data_dir, filename), 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")


# save_to_json(data, json_file)
save_to_json(draft_results, 'draft_results.json')
save_to_json(standings, 'standings.json')
save_to_json(teams, 'teams.json')
save_to_json(data, 'extracted_data.json')
print('Data saved to json files')
