#!/usr/bin/env python3
"""
analyze_category_trends.py - Analyze fantasy baseball category performance trends

This script analyzes category performance data from your fantasy baseball team,
identifying strengths, weaknesses, and trends over time. It generates visualizations
and insights to help inform your fantasy baseball decision-making.
"""

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import glob
from pathlib import Path

# Configuration
CATEGORIES = ['R', 'H', 'HR', 'RBI', 'SB', 'AVG', 'OPS', 'XBH', 'W', 'SV', 'K', 'ERA', 'WHIP', 'QS']
REVERSE_CATEGORIES = ['ERA', 'WHIP']  # Categories where lower is better
DATA_DIR = Path('./data')
OUTPUT_DIR = Path('./data/analysis')
VISUALIZATIONS_DIR = Path('./data/visualizations')

# Ensure directories exist
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
VISUALIZATIONS_DIR.mkdir(exist_ok=True, parents=True)


def load_data():
    """Load and combine data from all date directories"""
    print("Loading data from date directories...")
    
    # Find all date directories
    date_dirs = [d for d in DATA_DIR.glob('*') if d.is_dir() and d.name[0].isdigit()]
    
    if not date_dirs:
        print("No date directories found. Please run the Yahoo API script first.")
        return None
    
    # Sort directories by date
    date_dirs.sort()
    
    # Initialize data structures
    all_standings = []
    all_teams = []
    
    # Load data from each directory
    for date_dir in date_dirs:
        date_str = date_dir.name
        
        # Load standings data
        standings_file = date_dir / 'standings.json'
        if standings_file.exists():
            try:
                with open(standings_file, 'r') as f:
                    standings = json.load(f)
                    # Add date to each record
                    for team in standings:
                        team['date'] = date_str
                    all_standings.extend(standings)
            except Exception as e:
                print(f"Error loading standings from {date_str}: {e}")
        
        # Load teams data
        teams_file = date_dir / 'teams.json'
        if teams_file.exists():
            try:
                with open(teams_file, 'r') as f:
                    teams = json.load(f)
                    # Add date to each record
                    for team_id, team_data in teams.items():
                        team_data['date'] = date_str
                        team_data['team_id'] = team_id
                        all_teams.append(team_data)
            except Exception as e:
                print(f"Error loading teams from {date_str}: {e}")
    
    # Convert to DataFrames
    standings_df = pd.DataFrame(all_standings)
    teams_df = pd.DataFrame(all_teams)
    
    print(f"Loaded data from {len(date_dirs)} date directories.")
    
    return {
        'standings': standings_df,
        'teams': teams_df
    }


def extract_my_team_data(data, my_team_name):
    """Extract data for your team"""
    print(f"Extracting data for team: {my_team_name}")
    
    # Find your team in the teams data
    teams_df = data['teams']
    my_team = teams_df[teams_df['name'] == my_team_name]
    
    if my_team.empty:
        print(f"Team '{my_team_name}' not found in the data.")
        return None
    
    # Get your team's standings over time
    standings_df = data['standings']
    my_standings = standings_df[standings_df['name'] == my_team_name]
    
    # Sort by date
    my_standings = my_standings.sort_values('date')
    
    return {
        'team_info': my_team,
        'standings': my_standings
    }


def analyze_category_performance(my_team_data, data):
    """Analyze category performance for your team"""
    print("Analyzing category performance...")
    
    my_standings = my_team_data['standings']
    all_standings = data['standings']
    
    # Calculate league averages for each category by date
    league_avgs = all_standings.groupby('date')[CATEGORIES].mean().reset_index()
    
    # Merge with your team's data
    performance = pd.merge(my_standings, league_avgs, on='date', suffixes=('', '_league_avg'))
    
    # Calculate differentials
    for cat in CATEGORIES:
        if cat in REVERSE_CATEGORIES:
            # For categories where lower is better
            performance[f'{cat}_diff'] = performance[f'{cat}_league_avg'] - performance[cat]
        else:
            # For categories where higher is better
            performance[f'{cat}_diff'] = performance[cat] - performance[f'{cat}_league_avg']
    
    # Calculate 7-day rolling averages
    if len(performance) >= 7:
        for cat in CATEGORIES:
            performance[f'{cat}_7day'] = performance[cat].rolling(7, min_periods=1).mean()
    
    # Identify strengths and weaknesses
    latest = performance.iloc[-1]
    strengths = []
    weaknesses = []
    
    for cat in CATEGORIES:
        diff = latest[f'{cat}_diff']
        if diff > 0:
            strengths.append((cat, diff))
        else:
            weaknesses.append((cat, diff))
    
    # Sort by magnitude of difference
    strengths.sort(key=lambda x: x[1], reverse=True)
    weaknesses.sort(key=lambda x: x[1])
    
    return {
        'performance': performance,
        'strengths': strengths,
        'weaknesses': weaknesses
    }


def generate_visualizations(analysis):
    """Generate visualizations of category performance"""
    print("Generating visualizations...")
    
    performance = analysis['performance']
    
    # Create output directory if it doesn't exist
    VISUALIZATIONS_DIR.mkdir(exist_ok=True, parents=True)
    
    # 1. Category Performance vs. League Average
    plt.figure(figsize=(15, 10))
    
    for i, cat in enumerate(CATEGORIES):
        plt.subplot(4, 4, i+1)
        
        # Plot your team's performance
        plt.plot(performance['date'], performance[cat], 'b-', label='Your Team')
        
        # Plot league average
        plt.plot(performance['date'], performance[f'{cat}_league_avg'], 'r--', label='League Avg')
        
        plt.title(cat)
        plt.xticks(rotation=45)
        if i == 0:
            plt.legend()
    
    plt.tight_layout()
    plt.savefig(VISUALIZATIONS_DIR / 'category_vs_league.png')
    
    # 2. Category Differentials Over Time
    plt.figure(figsize=(15, 10))
    
    for i, cat in enumerate(CATEGORIES):
        plt.subplot(4, 4, i+1)
        
        # Plot differential
        plt.plot(performance['date'], performance[f'{cat}_diff'], 'g-')
        
        # Add a horizontal line at 0
        plt.axhline(y=0, color='r', linestyle='-')
        
        plt.title(f'{cat} Differential')
        plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig(VISUALIZATIONS_DIR / 'category_differentials.png')
    
    # 3. Strengths and Weaknesses Bar Chart
    plt.figure(figsize=(12, 8))
    
    # Combine strengths and weaknesses
    all_diffs = analysis['strengths'] + analysis['weaknesses']
    cats = [x[0] for x in all_diffs]
    diffs = [x[1] for x in all_diffs]
    
    # Create bar chart
    bars = plt.bar(cats, diffs)
    
    # Color bars based on positive/negative
    for i, bar in enumerate(bars):
        if diffs[i] > 0:
            bar.set_color('green')
        else:
            bar.set_color('red')
    
    plt.axhline(y=0, color='black', linestyle='-')
    plt.title('Category Strengths and Weaknesses')
    plt.ylabel('Differential from League Average')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig(VISUALIZATIONS_DIR / 'strengths_weaknesses.png')
    
    print(f"Visualizations saved to {VISUALIZATIONS_DIR}")


def generate_report(analysis):
    """Generate a text report of category analysis"""
    print("Generating category analysis report...")
    
    strengths = analysis['strengths']
    weaknesses = analysis['weaknesses']
    performance = analysis['performance']
    
    # Format the report
    report = []
    report.append("# Fantasy Baseball Category Analysis Report")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Team Strengths
    report.append("## Category Strengths")
    for cat, diff in strengths:
        if cat in REVERSE_CATEGORIES:
            report.append(f"- **{cat}**: {performance.iloc[-1][cat]:.3f} ({diff:.3f} better than league average)")
        else:
            report.append(f"- **{cat}**: {performance.iloc[-1][cat]:.3f} ({diff:.3f} above league average)")
    
    report.append("")
    
    # Team Weaknesses
    report.append("## Category Weaknesses")
    for cat, diff in weaknesses:
        if cat in REVERSE_CATEGORIES:
            report.append(f"- **{cat}**: {performance.iloc[-1][cat]:.3f} ({-diff:.3f} worse than league average)")
        else:
            report.append(f"- **{cat}**: {performance.iloc[-1][cat]:.3f} ({-diff:.3f} below league average)")
    
    report.append("")
    
    # Trending Analysis
    report.append("## Category Trends")
    
    # Only do trend analysis if we have enough data points
    if len(performance) >= 3:
        for cat in CATEGORIES:
            # Get the last few data points
            recent = performance[cat].tail(3).values
            
            # Determine trend
            if recent[-1] > recent[0]:
                trend = "Improving"
                emoji = "📈"
            elif recent[-1] < recent[0]:
                trend = "Declining"
                emoji = "📉"
            else:
                trend = "Stable"
                emoji = "➡️"
            
            report.append(f"- **{cat}**: {trend} {emoji}")
    
    report.append("")
    
    # Strategic Recommendations
    report.append("## Strategic Recommendations")
    
    # Recommend focusing on worst categories that aren't too far behind
    fixable_weaknesses = [cat for cat, diff in weaknesses if abs(diff) < 0.5]
    if fixable_weaknesses:
        report.append("### Categories to Target for Improvement")
        for cat in fixable_weaknesses[:3]:
            report.append(f"- **{cat}**: Close enough to league average to improve with targeted moves")
    
    # Recommend leveraging strengths
    if strengths:
        report.append("### Categories to Leverage")
        for cat, _ in strengths[:3]:
            report.append(f"- **{cat}**: Consider trading excess value to address weaknesses")
    
    # Write report to file
    report_path = OUTPUT_DIR / 'category_analysis.md'
    with open(report_path, 'w') as f:
        f.write('\n'.join(report))
    
    print(f"Report saved to {report_path}")
    
    return '\n'.join(report)


def main():
    """Main function to run the analysis"""
    print("Starting category trend analysis...")
    
    # Load data
    data = load_data()
    if not data:
        return
    
    # Get your team name
    # TODO: Replace with your actual team name or get from config
    my_team_name = "Your Team Name"
    
    # Extract your team's data
    my_team_data = extract_my_team_data(data, my_team_name)
    if not my_team_data:
        return
    
    # Analyze category performance
    analysis = analyze_category_performance(my_team_data, data)
    
    # Generate visualizations
    generate_visualizations(analysis)
    
    # Generate report
    report = generate_report(analysis)
    
    print("Category trend analysis complete!")
    print(report)


if __name__ == "__main__":
    main()
