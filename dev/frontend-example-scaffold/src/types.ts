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
}

export interface Player {
  name: string;
  position: string;
  team: string;
  round?: number;
  pickNumber?: number;
}

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