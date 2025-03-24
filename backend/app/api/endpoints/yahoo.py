from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import yahoo_service

router = APIRouter()


@router.get("/initialize")
async def initialize_yahoo_api():
    """Initialize the Yahoo Fantasy API connection"""
    success = yahoo_service.initialize()
    if not success:
        raise HTTPException(status_code=500, detail="Failed to initialize Yahoo Fantasy API")
    return {"status": "success", "message": "Yahoo Fantasy API initialized successfully"}


@router.get("/teams")
async def get_teams():
    """Get all teams in the league"""
    teams = yahoo_service.get_teams()
    if not teams:
        raise HTTPException(status_code=500, detail="Failed to get teams")
    return teams


@router.get("/standings")
async def get_standings():
    """Get current standings"""
    standings = yahoo_service.get_standings()
    if not standings:
        raise HTTPException(status_code=500, detail="Failed to get standings")
    return standings


@router.get("/draft")
async def get_draft_results():
    """Get draft results"""
    draft_results = yahoo_service.get_draft_results()
    if not draft_results:
        raise HTTPException(status_code=500, detail="Failed to get draft results")
    return draft_results


@router.get("/roster/{team_key}")
async def get_roster(team_key: str):
    """Get roster for a team"""
    roster = yahoo_service.get_roster(team_key)
    if not roster:
        raise HTTPException(status_code=500, detail="Failed to get roster")
    return roster


@router.get("/settings")
async def get_league_settings():
    """Get league settings"""
    settings = yahoo_service.get_league_settings()
    if not settings:
        raise HTTPException(status_code=500, detail="Failed to get league settings")
    return settings


@router.post("/collect-data")
async def collect_data(background_tasks: BackgroundTasks):
    """Collect all data from Yahoo Fantasy API and save to JSON files"""

    # Add data collection task to background tasks
    background_tasks.add_task(collect_and_save_data)

    return {"status": "success", "message": "Data collection started in background"}


async def collect_and_save_data():
    """Background task to collect and save data"""
    # Initialize Yahoo API if not already initialized
    if not yahoo_service.game or not yahoo_service.league:
        yahoo_service.initialize()

    # Collect data
    data = yahoo_service.collect_data()
    if not data:
        return

    # Save individual data files
    yahoo_service.save_data_to_json(data["teams"], "teams.json")
    yahoo_service.save_data_to_json(data["standings"], "standings.json")
    yahoo_service.save_data_to_json(data["draft_results"], "draft_results.json")
    yahoo_service.save_data_to_json(data["rosters"], "rosters.json")
    yahoo_service.save_data_to_json(data["settings"], "settings.json")

    # Save combined data
    yahoo_service.save_data_to_json(data, "combined_data.json")
