Your decision to drop **Austin Wells** for **Victor Scott II** and **Drew Rasmussen** for **AJ Smith-Shawver** is bold but strategically sound given your league's setup and needs. Here's an analysis of the risks and potential rewards of this approach:

---

## **Move 1: Dropping Austin Wells for Victor Scott II**

### **Rationale**

1. **Steals Category Impact**:
   - Victor Scott II addresses a critical need in stolen bases, a category where your roster was relatively weak.
   - His elite speed (99th percentile sprint speed) gives you a significant edge in SB, a standalone category in your league.

2. **Catcher Depth**:
   - Carrying two catchers (Wells and Contreras) in a one-catcher league was suboptimal.
   - While Wells has upside, his time-share situation with the Yankees limits his immediate fantasy value.
   - Contreras is durable enough to anchor the position, making Wells expendable.

3. **Category Balance**:
   - Scott II's elite speed adds a unique skill set that complements your roster, while Wells' value as a second catcher was redundant.

### **Risk Assessment**

- If Contreras suffers an injury, you'll need to stream or replace a catcher midseason.
- Scott's batting average risk (.220–.240 projected) could hurt your AVG category slightly, but his SB upside outweighs this downside.

---

## **Move 2: Dropping Drew Rasmussen for AJ Smith-Shawver**

### **Rationale**

1. **Pitching Depth and Upside**:
   - Rasmussen’s injury history (internal brace surgery) and limited innings projection made him unreliable.
   - Smith-Shawver offers immediate value as part of the Braves' rotation, with strong spring performance (20 K/5 BB in 16 IP) and high strikeout potential.

2. **Short-Term Production**:
   - Smith-Shawver’s rotation spot might be temporary (until Spencer Strider returns), but he can help you dominate Ks and ratios in the short term.
   - Rasmussen’s return from injury is uncertain, and even if healthy, his role could be limited by Tampa Bay’s pitching philosophy.# Fantasy Baseball Decision Log

A comprehensive system for tracking, analyzing, and improving fantasy baseball decisions throughout the season.

## Overview

This project provides a structured approach to maintaining a fantasy baseball decision log, helping you track your draft choices, waiver wire moves, lineup decisions, and trades. By documenting your thought process and analyzing the outcomes, you can identify patterns in your decision-making and improve your fantasy baseball management skills over time.

The system is specifically designed for a 12-team, categories-based H2H league with daily lineup changes and a maximum of 7 waiver moves per week.

## Features

- **Structured Decision Templates**: Standardized templates for documenting different types of fantasy baseball decisions
- **Yahoo Fantasy API Integration**: Automated data collection from your Yahoo Fantasy Baseball league
- **Category Performance Analysis**: Tools to analyze your team's performance across different statistical categories
- **Waiver Wire Recommendations**: Identification of available players who could address your team's weaknesses
- **Visual Analytics**: Graphical representations of your team's performance and category trends

## Project Structure

```
fantasy-baseball-log/
├── data/                       # Raw data from Yahoo Fantasy API
│   ├── YYYY-MM-DD/             # Date-based directories for historical data
│   ├── roster-snapshots/       # Daily roster snapshots
│   ├── player-stats/           # Player statistics
│   ├── category-performance/   # Category performance data
│   ├── analysis/               # Analysis outputs
│   └── visualizations/         # Generated charts and graphs
├── decisions/                  # Decision log entries
│   ├── draft/                  # Draft analysis
│   ├── waiver-moves/           # Waiver wire decisions
│   └── trades/                 # Trade analysis
├── templates/                  # Templates for decision logs
│   ├── draft-analysis-template.md
│   ├── waiver-move-template.md
│   ├── daily-lineup-template.md
│   ├── trade-analysis-template.md
│   ├── weekly-review-template.md
│   └── monthly-review-template.md
├── scripts/                    # Analysis and data collection scripts
│   ├── yahoo_oauth.experimental.py  # Yahoo Fantasy API authentication
│   ├── analyze_category_trends.py   # Category performance analysis
│   └── find_waiver_opportunities.py # Waiver wire recommendations
└── docs/                       # Documentation
    └── SPECIFICATION.md        # Project specifications
```

## Getting Started

### Prerequisites

- Python 3.8+
- Yahoo Fantasy Baseball account
- Yahoo Developer App credentials

### Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/fantasy-baseball-log.git
   cd fantasy-baseball-log
   ```

2. Install required packages:

   ```
   pip install -r requirements.txt
   ```

3. Set up Yahoo API credentials:
   - Create a Yahoo Developer App at <https://developer.yahoo.com/apps/>
   - Create a `.env` file with your credentials:

     ```
     YAHOO_CLIENT_ID=your_client_id
     YAHOO_CLIENT_SECRET=your_client_secret
     YAHOO_REDIRECT_URI=https://localhost:8000/callback
     ```

### Usage

#### Initial Setup

1. Run the Yahoo OAuth script to authenticate with the Yahoo Fantasy API:

   ```
   python scripts/yahoo_oauth.experimental.py
   ```

   This will create an `oauth2.json` file with your authentication tokens.

#### Decision Logging

1. **Draft Analysis**:
   - Copy `templates/draft-analysis-template.md` to `decisions/draft/YYYY-draft-analysis.md`
   - Fill in the template with your draft analysis

2. **Waiver Wire Moves**:
   - Copy `templates/waiver-move-template.md` to `decisions/waiver-moves/YYYY-MM-DD-player-for-player.md`
   - Document your waiver wire decision

3. **Daily Lineup Decisions**:
   - Copy `templates/daily-lineup-template.md` to `decisions/lineups/YYYY-MM-DD-lineup.md`
   - Record your lineup decisions and matchup considerations

4. **Trade Analysis**:
   - Copy `templates/trade-analysis-template.md` to `decisions/trades/YYYY-MM-DD-trade-description.md`
   - Document your trade analysis

#### Analysis

1. Analyze category performance trends:

   ```
   python scripts/analyze_category_trends.py
   ```

   This will generate visualizations and a report in `data/analysis/category_analysis.md`.

2. Find waiver wire opportunities:

   ```
   python scripts/find_waiver_opportunities.py
   ```

   This will generate recommendations in `data/analysis/waiver_recommendations.md`.

## Review Process

For maximum benefit, follow this review schedule:

1. **Daily Quick Review** (5 minutes):
   - Update lineup decisions and immediate results
   - Make notes on waiver wire targets

2. **Weekly Comprehensive Review** (30 minutes):
   - Analyze matchup results against strategies employed
   - Review waiver wire decisions and their initial impact
   - Plan strategy for upcoming matchup

3. **Monthly Deep Dive** (1 hour):
   - Identify patterns in successful and unsuccessful decisions
   - Compare player performance against draft expectations
   - Evaluate category strengths/weaknesses and adjust strategy accordingly

4. **Mid-Season Audit** (2 hours):
   - Comprehensive analysis of all decisions to date
   - Identify your tendencies and biases
   - Adjust strategy for second half of season

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
