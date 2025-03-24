# Fantasy Baseball Decision Log

A comprehensive tool for tracking and analyzing fantasy baseball decisions throughout the season.

## Overview

The Fantasy Baseball Decision Log is designed to help fantasy baseball managers track their decisions (draft picks, waiver moves, trades, lineup changes) and analyze their impact over time. The application integrates with the Yahoo Fantasy API to fetch league data and provides tools for analysis and decision-making.

## Features

- **Decision Logging**: Track draft analysis, waiver wire moves, trades, and lineup decisions
- **Yahoo Fantasy API Integration**: Fetch real-time data from your Yahoo Fantasy Baseball league
- **Data Analysis**: Analyze category trends, player performance, and team statistics
- **Waiver Wire Recommendations**: Get suggestions for waiver wire pickups based on team needs

## Project Structure

The project is organized into two main components:

### Backend (Python/FastAPI)

- RESTful API built with FastAPI
- SQLite database for development, PostgreSQL for production
- Yahoo Fantasy API integration
- Data analysis and processing

### Frontend (React/TypeScript/Vite)

- Modern React application with TypeScript
- Vite for fast development and building
- Tailwind CSS for styling
- React Query for data fetching and caching

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- Bun (for frontend package management)
- uv (for Python package management)
- Docker and Docker Compose (optional, for PostgreSQL)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/jimbrig/fantasy-baseball-log.git
cd fantasy-baseball-log
```

2. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your Yahoo API credentials and other settings
```

3. Install backend dependencies:

```bash
cd backend
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

4. Install frontend dependencies:

```bash
cd frontend
bun install
```

### Running the Application

#### Backend

```bash
cd backend
python run.py --reload
```

The API will be available at http://localhost:8000.

#### Frontend

```bash
cd frontend
bun run dev
```

The frontend will be available at http://localhost:5173.

#### Database (PostgreSQL)

If you want to use PostgreSQL instead of SQLite:

```bash
cd docker
docker-compose up -d
```

Then update the `DATABASE_URL` in your `.env` file.

## Yahoo Fantasy API Setup

1. Create a Yahoo Developer account at https://developer.yahoo.com/
2. Create a new application
3. Set the application domain to `localhost`
4. Set the redirect URI to `oob` (out of band)
5. Copy the Client ID and Client Secret to your `.env` file

## Development

### Backend

- FastAPI with automatic OpenAPI documentation
- SQLAlchemy ORM for database operations
- Pydantic for data validation
- Yahoo Fantasy API integration

### Frontend

- React with TypeScript
- Vite for fast development
- React Query for data fetching
- React Router for navigation
- Tailwind CSS for styling

## License

MIT
