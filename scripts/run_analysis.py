#!/usr/bin/env python3
"""
run_analysis.py - Run analysis tools for fantasy baseball decision log

This script provides a simple interface to run the various analysis tools
for the fantasy baseball decision log system.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# Configuration
SCRIPTS_DIR = Path('./scripts')
DATA_DIR = Path('./data')
ANALYSIS_DIR = Path('./data/analysis')
VISUALIZATIONS_DIR = Path('./data/visualizations')

# Ensure directories exist
ANALYSIS_DIR.mkdir(exist_ok=True, parents=True)
VISUALIZATIONS_DIR.mkdir(exist_ok=True, parents=True)

# Available analysis tools
ANALYSIS_TOOLS = {
    'category': {
        'script': 'analyze_category_trends.py',
        'description': 'Analyze category performance trends',
        'output': 'category_analysis.md'
    },
    'waiver': {
        'script': 'find_waiver_opportunities.py',
        'description': 'Find waiver wire opportunities based on category needs',
        'output': 'waiver_recommendations.md'
    },
    'collect': {
        'script': 'daily_data_collection.py',
        'description': 'Collect daily data from Yahoo Fantasy API',
        'output': None
    }
}


def list_analysis_tools():
    """List available analysis tools"""
    print("Available analysis tools:")
    for name, info in ANALYSIS_TOOLS.items():
        print(f"  {name}: {info['description']}")
        if info['output']:
            print(f"    Output: {ANALYSIS_DIR / info['output']}")
    print("\nUsage: python run_analysis.py [tool_name]")
    print("       python run_analysis.py all")


def run_tool(tool_name):
    """Run a specific analysis tool"""
    if tool_name not in ANALYSIS_TOOLS:
        print(f"Error: Unknown tool '{tool_name}'")
        list_analysis_tools()
        return False
    
    tool_info = ANALYSIS_TOOLS[tool_name]
    script_path = SCRIPTS_DIR / tool_info['script']
    
    if not script_path.exists():
        print(f"Error: Script not found: {script_path}")
        return False
    
    print(f"Running {tool_info['description']}...")
    
    try:
        # Run the script
        result = subprocess.run(['python', str(script_path)], check=True)
        
        if result.returncode == 0:
            print(f"Successfully ran {tool_name} analysis")
            
            # Check if output file exists
            if tool_info['output']:
                output_path = ANALYSIS_DIR / tool_info['output']
                if output_path.exists():
                    print(f"Output saved to: {output_path}")
                    
                    # Ask if user wants to view the output
                    view = input("View output? (y/n): ")
                    if view.lower() == 'y':
                        # Try to open the file with the default application
                        try:
                            if os.name == 'nt':  # Windows
                                os.startfile(output_path)
                            elif os.name == 'posix':  # macOS or Linux
                                subprocess.run(['open' if sys.platform == 'darwin' else 'xdg-open', str(output_path)])
                        except Exception as e:
                            print(f"Error opening file: {e}")
            
            return True
        else:
            print(f"Error running {tool_name} analysis")
            return False
    
    except subprocess.CalledProcessError as e:
        print(f"Error running {tool_name} analysis: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def run_all_tools():
    """Run all analysis tools"""
    success = True
    
    for tool_name in ANALYSIS_TOOLS:
        print(f"\nRunning {tool_name}...")
        if not run_tool(tool_name):
            success = False
    
    return success


def main():
    """Main function to parse arguments and run analysis tools"""
    parser = argparse.ArgumentParser(description='Run analysis tools for fantasy baseball decision log')
    parser.add_argument('tool', nargs='?', help='Name of the analysis tool to run')
    
    args = parser.parse_args()
    
    if not args.tool:
        list_analysis_tools()
        return 0
    
    if args.tool.lower() == 'all':
        success = run_all_tools()
    else:
        success = run_tool(args.tool)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
