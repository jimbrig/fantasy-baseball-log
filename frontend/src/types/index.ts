// Decision types
export type DecisionType = 'draft' | 'waiver' | 'trade' | 'lineup' | 'general';

export interface Decision {
  id: string;
  type: DecisionType;
  date: string;
  title: string;
  description: string;
  impact: string;
  result?: string;
  categories?: string[];
  content?: string; // Markdown content
  created_at: string;
  updated_at: string;
}

export type DecisionCreate = Omit<Decision, 'id' | 'created_at' | 'updated_at'>;

export type DecisionUpdate = Partial<DecisionCreate>;

// Player types
export interface Player {
  name: string;
  position: string;
  team: string;
  round?: number;
  pickNumber?: number;
  stats?: Record<string, number | string>;
}

// Yahoo Fantasy API types
export interface YahooTeam {
  team_key: string;
  name: string;
  number_of_moves: string;
  number_of_trades: string;
  roster_adds: {
    coverage_type: string;
    coverage_value: string;
    value: string;
  };
  league_scoring_type: string;
  managers: Array<{
    manager_id: string;
    nickname: string;
  }>;
}

export interface YahooLeague {
  league_key: string;
  name: string;
  num_teams: number;
  current_week: number;
  start_week: number;
  end_week: number;
  is_finished: boolean;
  settings: {
    roster_positions: Array<{
      position: string;
      count: number;
    }>;
    stat_categories: Array<{
      name: string;
      display_name: string;
    }>;
  };
}

// Analysis types
export interface CategoryAnalysis {
  category: string;
  value: number;
  leagueAverage: number;
  differential: number;
  trend: 'improving' | 'declining' | 'stable';
}

export interface WaiverRecommendation {
  player: Player;
  score: number;
  categories: string[];
  reason: string;
}

export interface TeamStats {
  categories: Record<string, number>;
  strengths: CategoryAnalysis[];
  weaknesses: CategoryAnalysis[];
}

export interface RosterPlayer extends Player {
  stats: Record<string, number | string>;
  projections?: Record<string, number | string>;
  trends?: Record<string, 'up' | 'down' | 'stable'>;
}

export interface Roster {
  players: RosterPlayer[];
  lastUpdated: string;
}
