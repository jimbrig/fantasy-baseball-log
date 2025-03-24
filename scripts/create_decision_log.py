#!/usr/bin/env python3
"""
create_decision_log.py - Helper script to create new decision log entries from templates

This script helps users create new decision log entries by copying the appropriate
template to the correct location and pre-filling some basic information.
"""

import os
import sys
import shutil
from datetime import datetime
from pathlib import Path
import argparse

# Configuration
TEMPLATES_DIR = Path('./templates')
DECISIONS_DIR = Path('./decisions')

# Template mapping
TEMPLATE_MAPPING = {
    'waiver': {
        'template': 'waiver-move-template.md',
        'directory': 'waiver-moves',
        'filename_format': '{date}-{player1}-for-{player2}.md'
    },
    'draft': {
        'template': 'draft-analysis-template.md',
        'directory': 'draft',
        'filename_format': '{date}-draft-analysis.md'
    },
    'lineup': {
        'template': 'daily-lineup-template.md',
        'directory': 'lineups',
        'filename_format': '{date}-lineup.md'
    },
    'trade': {
        'template': 'trade-analysis-template.md',
        'directory': 'trades',
        'filename_format': '{date}-{description}.md'
    },
    'weekly': {
        'template': 'weekly-review-template.md',
        'directory': 'reviews',
        'filename_format': '{date}-week-{week}-review.md'
    },
    'monthly': {
        'template': 'monthly-review-template.md',
        'directory': 'reviews',
        'filename_format': '{date}-{month}-review.md'
    }
}


def create_decision_log(decision_type, **kwargs):
    """Create a new decision log entry from a template"""
    if decision_type not in TEMPLATE_MAPPING:
        print(f"Error: Unknown decision type '{decision_type}'")
        print(f"Available types: {', '.join(TEMPLATE_MAPPING.keys())}")
        return False
    
    # Get template info
    template_info = TEMPLATE_MAPPING[decision_type]
    template_path = TEMPLATES_DIR / template_info['template']
    
    # Check if template exists
    if not template_path.exists():
        print(f"Error: Template file not found: {template_path}")
        return False
    
    # Create directory if it doesn't exist
    output_dir = DECISIONS_DIR / template_info['directory']
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Get current date if not provided
    if 'date' not in kwargs:
        kwargs['date'] = datetime.now().strftime('%Y-%m-%d')
    
    # Create filename
    try:
        filename = template_info['filename_format'].format(**kwargs)
    except KeyError as e:
        print(f"Error: Missing required parameter: {e}")
        return False
    
    # Full output path
    output_path = output_dir / filename
    
    # Check if file already exists
    if output_path.exists():
        overwrite = input(f"File already exists: {output_path}\nOverwrite? (y/n): ")
        if overwrite.lower() != 'y':
            print("Operation cancelled.")
            return False
    
    # Copy template to output file
    shutil.copy(template_path, output_path)
    
    # Read the template content
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace placeholders with provided values
    replacements = {
        '[DATE]': kwargs.get('date', datetime.now().strftime('%Y-%m-%d')),
        '[YEAR]': kwargs.get('year', datetime.now().strftime('%Y')),
        '[WEEK NUMBER]': kwargs.get('week', ''),
        '[MONTH]': kwargs.get('month', datetime.now().strftime('%B')),
    }
    
    # Add decision-specific replacements
    if decision_type == 'waiver':
        replacements['[TITLE]'] = f"Adding {kwargs.get('player1', '')} for {kwargs.get('player2', '')}"
        replacements['[PLAYER BEING ADDED]'] = kwargs.get('player1', '')
        replacements['[PLAYER BEING DROPPED]'] = kwargs.get('player2', '')
    elif decision_type == 'trade':
        replacements['[BRIEF TRADE DESCRIPTION]'] = kwargs.get('description', '')
    
    # Apply replacements
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    
    # Write updated content back to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Created new {decision_type} decision log: {output_path}")
    return True


def main():
    """Main function to parse arguments and create decision log"""
    parser = argparse.ArgumentParser(description='Create a new fantasy baseball decision log entry')
    parser.add_argument('type', choices=TEMPLATE_MAPPING.keys(), help='Type of decision log to create')
    parser.add_argument('--date', help='Date for the decision log (default: today)')
    
    # Decision-specific arguments
    parser.add_argument('--player1', help='Player being added (for waiver moves)')
    parser.add_argument('--player2', help='Player being dropped (for waiver moves)')
    parser.add_argument('--description', help='Brief description (for trades)')
    parser.add_argument('--week', help='Week number (for weekly reviews)')
    parser.add_argument('--month', help='Month name (for monthly reviews)')
    parser.add_argument('--year', help='Year (for draft analysis)')
    
    args = parser.parse_args()
    
    # Convert args to dictionary
    kwargs = {k: v for k, v in vars(args).items() if v is not None and k != 'type'}
    
    # Create decision log
    success = create_decision_log(args.type, **kwargs)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
