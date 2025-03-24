#!/usr/bin/env python3
"""
find_waiver_opportunities.py - Find waiver wire opportunities based on category needs

This script analyzes your team's category strengths and weaknesses, then identifies
available players who could help address your weaknesses. It uses data from the Yahoo
Fantasy API and provides recommendations for waiver wire pickups.
"""

import os
import json
import pandas as pd
import numpy as np
from pathlib import Path
import yahoo_fantasy_api as yfa
from yahoo_oauth import OAuth2
from dotenv import load_dotenv
import datetime

# Load environment variables
load_dotenv()

# Configuration
DATA_DIR = Path('./data')
OUTPUT_DIR = Path('./data/analysis')
CATEGORIES = ['R', 'H', 'HR', 'RBI', 'SB', 'AVG', 'OPS', 'XBH', 'W', 'SV', 'K', 'ERA', 'WHIP', 'QS']
REVERSE_CATEGORIES = ['ERA', 'WHIP']  # Categories where lower is better

# Ensure directories exist
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)


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


def get_team_data(lg):
    """Get team data from Yahoo Fantasy API"""
    print("Fetching team data...")
    
    try:
        # Get team key
        team_key = lg.team_key()
        
        # Get team data
        team = lg.to_team(team_key)
        
        # Get roster
        roster = team.roster()
        
        # Get team standings
        standings = lg.standings()
        my_standings = next((team for team in standings if team['team_key'] == team_key), None)
        
        return {
            'team': team,
            'roster': roster,
            'standings': my_standings
        }
    
    except Exception as e:
        print(f"Error fetching team data: {e}")
        return None


def identify_category_needs(team_data):
    """Identify category needs based on team standings"""
    print("Identifying category needs...")
    
    standings = team_data['standings']
    
    if not standings:
        print("No standings data found.")
        return None
    
    # Extract category values
    category_values = {}
    for cat in CATEGORIES:
        if cat in standings:
            category_values[cat] = standings[cat]
    
    # Calculate league averages (this would ideally come from all teams' data)
    # For now, we'll use placeholder values
    league_averages = {
        'R': 500,
        'H': 1000,
        'HR': 150,
        'RBI': 500,
        'SB': 100,
        'AVG': 0.265,
        'OPS': 0.750,
        'XBH': 300,
        'W': 70,
        'SV': 30,
        'K': 1000,
        'ERA': 3.80,
        'WHIP': 1.25,
        'QS': 60
    }
    
    # Calculate differentials
    differentials = {}
    for cat in CATEGORIES:
        if cat in category_values and cat in league_averages:
            if cat in REVERSE_CATEGORIES:
                # For categories where lower is better
                differentials[cat] = league_averages[cat] - category_values[cat]
            else:
                # For categories where higher is better
                differentials[cat] = category_values[cat] - league_averages[cat]
    
    # Sort categories by differential
    sorted_diffs = sorted(differentials.items(), key=lambda x: x[1])
    
    # Identify weakest categories
    weakest_categories = [cat for cat, diff in sorted_diffs[:3]]
    
    print(f"Identified weakest categories: {', '.join(weakest_categories)}")
    
    return {
        'category_values': category_values,
        'differentials': differentials,
        'weakest_categories': weakest_categories
    }


def get_available_players(lg, positions=None):
    """Get available players from Yahoo Fantasy API"""
    print("Fetching available players...")
    
    if positions is None:
        positions = ['C', '1B', '2B', '3B', 'SS', 'OF', 'SP', 'RP']
    
    all_players = []
    
    try:
        for position in positions:
            print(f"Fetching {position} players...")
            
            # Get free agents for the position
            free_agents = lg.free_agents(position)
            
            # Add position to each player
            for player in free_agents:
                player['position'] = position
                all_players.append(player)
            
            print(f"Found {len(free_agents)} available {position} players")
        
        print(f"Total available players found: {len(all_players)}")
        return all_players
    
    except Exception as e:
        print(f"Error fetching available players: {e}")
        return []


def score_players_by_category_needs(players, category_needs):
    """Score players based on how well they address category needs"""
    print("Scoring players based on category needs...")
    
    weakest_categories = category_needs['weakest_categories']
    
    # Define category weights (higher for weaker categories)
    category_weights = {cat: 3 for cat in weakest_categories}
    for cat in CATEGORIES:
        if cat not in category_weights:
            category_weights[cat] = 1
    
    # Score each player
    scored_players = []
    
    for player in players:
        score = 0
        
        # Extract player stats
        stats = player.get('player_stats', {}).get('stats', [])
        
        # Convert stats to dictionary
        player_stats = {}
        for stat in stats:
            stat_id = stat.get('stat_id')
            stat_value = stat.get('value')
            
            # Map stat_id to category
            # This mapping would need to be adjusted based on Yahoo's stat IDs
            stat_mapping = {
                '60': 'R',
                '8': 'HR',
                '85': 'RBI',
                '16': 'SB',
                '3': 'AVG',
                '55': 'OPS',
                '13': 'W',
                '32': 'SV',
                '42': 'K',
                '50': 'ERA',
                '26': 'WHIP',
                '53': 'QS'
            }
            
            if stat_id in stat_mapping:
                category = stat_mapping[stat_id]
                player_stats[category] = stat_value
        
        # Calculate score based on category needs
        for cat, weight in category_weights.items():
            if cat in player_stats:
                # Convert stat value to float if possible
                try:
                    value = float(player_stats[cat])
                    
                    # Score based on category
                    if cat == 'HR' and value > 20:
                        score += 3 * weight
                    elif cat == 'SB' and value > 15:
                        score += 3 * weight
                    elif cat == 'AVG' and value > 0.280:
                        score += 2 * weight
                    elif cat == 'OPS' and value > 0.800:
                        score += 2 * weight
                    elif cat == 'ERA' and value < 3.50:
                        score += 3 * weight
                    elif cat == 'WHIP' and value < 1.20:
                        score += 3 * weight
                    elif cat == 'K' and value > 150:
                        score += 2 * weight
                    elif cat == 'W' and value > 10:
                        score += 2 * weight
                    elif cat == 'SV' and value > 20:
                        score += 3 * weight
                    elif cat == 'QS' and value > 15:
                        score += 2 * weight
                except (ValueError, TypeError):
                    pass
        
        # Add score to player data
        player['opportunity_score'] = score
        scored_players.append(player)
    
    # Sort players by score
    scored_players.sort(key=lambda x: x.get('opportunity_score', 0), reverse=True)
    
    print(f"Scored {len(scored_players)} players")
    
    return scored_players


def generate_recommendations(scored_players, category_needs, max_recommendations=10):
    """Generate recommendations based on scored players"""
    print("Generating recommendations...")
    
    weakest_categories = category_needs['weakest_categories']
    
    # Get top players overall
    top_players = scored_players[:max_recommendations]
    
    # Get top players by position
    top_by_position = {}
    for position in ['C', '1B', '2B', '3B', 'SS', 'OF', 'SP', 'RP']:
        position_players = [p for p in scored_players if p.get('position') == position]
        top_by_position[position] = position_players[:3]
    
    # Get top players by category
    top_by_category = {}
    for cat in weakest_categories:
        # This would require more detailed player stats
        # For now, we'll use a placeholder approach
        cat_players = sorted(
            [p for p in scored_players if p.get('opportunity_score', 0) > 0],
            key=lambda x: x.get('opportunity_score', 0),
            reverse=True
        )
        top_by_category[cat] = cat_players[:3]
    
    # Format recommendations
    recommendations = []
    
    recommendations.append("# Waiver Wire Recommendations")
    recommendations.append(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    recommendations.append("## Category Needs")
    for cat in weakest_categories:
        recommendations.append(f"- **{cat}**: {category_needs['category_values'].get(cat, 'N/A')}")
    
    recommendations.append("\n## Top Overall Recommendations")
    for i, player in enumerate(top_players, 1):
        name = player.get('name', 'Unknown Player')
        team = player.get('editorial_team_abbr', 'N/A')
        position = player.get('position', 'N/A')
        score = player.get('opportunity_score', 0)
        
        recommendations.append(f"{i}. **{name}** ({team}, {position}) - Score: {score}")
    
    recommendations.append("\n## Top Recommendations by Position")
    for position, players in top_by_position.items():
        if players:
            recommendations.append(f"\n### {position}")
            for i, player in enumerate(players, 1):
                name = player.get('name', 'Unknown Player')
                team = player.get('editorial_team_abbr', 'N/A')
                score = player.get('opportunity_score', 0)
                
                recommendations.append(f"{i}. **{name}** ({team}) - Score: {score}")
    
    recommendations.append("\n## Top Recommendations by Category Need")
    for cat, players in top_by_category.items():
        if players:
            recommendations.append(f"\n### {cat}")
            for i, player in enumerate(players, 1):
                name = player.get('name', 'Unknown Player')
                team = player.get('editorial_team_abbr', 'N/A')
                position = player.get('position', 'N/A')
                score = player.get('opportunity_score', 0)
                
                recommendations.append(f"{i}. **{name}** ({team}, {position}) - Score: {score}")
    
    # Write recommendations to file
    recommendations_path = OUTPUT_DIR / 'waiver_recommendations.md'
    with open(recommendations_path, 'w') as f:
        f.write('\n'.join(recommendations))
    
    print(f"Recommendations saved to {recommendations_path}")
    
    return '\n'.join(recommendations)


def main():
    """Main function to run the waiver wire analysis"""
    print("Starting waiver wire opportunity analysis...")
    
    # Connect to Yahoo API
    oauth = connect_to_yahoo_api()
    if not oauth:
        return
    
    # Get league data
    lg = get_league_data(oauth)
    if not lg:
        return
    
    # Get team data
    team_data = get_team_data(lg)
    if not team_data:
        return
    
    # Identify category needs
    category_needs = identify_category_needs(team_data)
    if not category_needs:
        return
    
    # Get available players
    available_players = get_available_players(lg)
    if not available_players:
        return
    
    # Score players based on category needs
    scored_players = score_players_by_category_needs(available_players, category_needs)
    
    # Generate recommendations
    recommendations = generate_recommendations(scored_players, category_needs)
    
    print("Waiver wire opportunity analysis complete!")
    print(recommendations)


if __name__ == "__main__":
    main()
