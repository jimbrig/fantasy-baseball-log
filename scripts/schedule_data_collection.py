#!/usr/bin/env python3
"""
schedule_data_collection.py - Schedule the daily data collection job

This script helps users set up a scheduled task to run the daily data collection
script automatically. It supports Windows (Task Scheduler) and Unix-like systems
(cron).
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import argparse

# Configuration
PROJECT_ROOT = Path('.')
SCRIPTS_DIR = PROJECT_ROOT / 'scripts'
DATA_COLLECTION_SCRIPT = SCRIPTS_DIR / 'daily_data_collection.py'


def setup_windows_task(time):
    """Set up a scheduled task on Windows using Task Scheduler"""
    print(f"Setting up Windows scheduled task to run at {time} daily...")

    # Get absolute paths
    script_path = DATA_COLLECTION_SCRIPT.resolve()
    python_path = sys.executable

    # Create the task name
    task_name = "FantasyBaseballDataCollection"

    # Parse the time
    hour, minute = time.split(':')

    # Create the command
    cmd = [
        'schtasks', '/create', '/tn', task_name, '/tr',
        f'"{python_path}" "{script_path}"',
        '/sc', 'daily', '/st', time, '/f'
    ]

    try:
        # Run the command
        subprocess.run(cmd, check=True)
        print(f"Scheduled task '{task_name}' created successfully.")
        print(f"The script will run daily at {time}.")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error creating scheduled task: {e}")
        print("You may need to run this script as administrator.")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def setup_unix_cron(time):
    """Set up a cron job on Unix-like systems"""
    print(f"Setting up cron job to run at {time} daily...")

    # Get absolute paths
    script_path = DATA_COLLECTION_SCRIPT.resolve()
    python_path = sys.executable

    # Parse the time
    hour, minute = time.split(':')

    # Create the cron entry
    cron_entry = f"{minute} {hour} * * * {python_path} {script_path} >> {PROJECT_ROOT}/data/cron.log 2>&1"

    try:
        # Get existing crontab
        existing_crontab = subprocess.check_output(['crontab', '-l'], stderr=subprocess.DEVNULL).decode('utf-8')
    except subprocess.CalledProcessError:
        # No existing crontab
        existing_crontab = ""

    # Check if the entry already exists
    if cron_entry in existing_crontab:
        print("Cron job already exists.")
        return True

    # Add the new entry
    new_crontab = existing_crontab.strip() + "\n" + cron_entry + "\n"

    try:
        # Write the new crontab
        process = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE)
        process.communicate(input=new_crontab.encode('utf-8'))

        if process.returncode == 0:
            print("Cron job created successfully.")
            print(f"The script will run daily at {time}.")
            return True
        else:
            print(f"Error creating cron job. Return code: {process.returncode}")
            return False

    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def main():
    """Main function to schedule the daily data collection job"""
    parser = argparse.ArgumentParser(description='Schedule the daily data collection job')
    parser.add_argument('--time', default='03:00', help='Time to run the job daily (HH:MM format, 24-hour clock)')

    args = parser.parse_args()

    # Validate the time format
    try:
        hour, minute = args.time.split(':')
        hour = int(hour)
        minute = int(minute)
        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            raise ValueError
    except ValueError:
        print("Error: Invalid time format. Please use HH:MM format (24-hour clock).")
        return 1

    # Check if the data collection script exists
    if not DATA_COLLECTION_SCRIPT.exists():
        print(f"Error: Data collection script not found at {DATA_COLLECTION_SCRIPT}")
        return 1

    # Determine the operating system
    system = platform.system()

    if system == 'Windows':
        success = setup_windows_task(args.time)
    elif system in ['Linux', 'Darwin']:  # Linux or macOS
        success = setup_unix_cron(args.time)
    else:
        print(f"Error: Unsupported operating system: {system}")
        return 1

    if success:
        print("\nData collection has been scheduled successfully.")
        print("\nTo verify the schedule:")
        if system == 'Windows':
            print("1. Open Task Scheduler")
            print("2. Look for the 'FantasyBaseballDataCollection' task")
        else:
            print("1. Run 'crontab -l' to view your crontab")

        print("\nTo manually run the data collection script:")
        print(f"python {DATA_COLLECTION_SCRIPT}")

        return 0
    else:
        print("\nFailed to schedule data collection.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
