import axios from 'axios';
import type { YahooTeam, YahooLeague } from '../types';

const YAHOO_API_BASE = 'https://fantasysports.yahooapis.com/fantasy/v2';
const LEAGUE_ID = import.meta.env.VITE_YAHOO_LEAGUE_ID;

class YahooFantasyService {
  private accessToken: string | null = null;

  setAccessToken(token: string) {
    this.accessToken = token;
    localStorage.setItem('yahoo_access_token', token);
  }

  getAccessToken(): string | null {
    return this.accessToken || localStorage.getItem('yahoo_access_token');
  }

  clearAccessToken() {
    this.accessToken = null;
    localStorage.removeItem('yahoo_access_token');
  }

  private async request<T>(endpoint: string): Promise<T> {
    const token = this.getAccessToken();
    if (!token) {
      throw new Error('Not authenticated');
    }

    try {
      const response = await axios.get(`${YAHOO_API_BASE}${endpoint}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Access-Control-Allow-Origin': '*',
        },
        params: {
          format: 'json',
        },
      });

      return response.data.fantasy_content;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.status === 401) {
        this.clearAccessToken();
      }
      throw error;
    }
  }

  async getTeam(teamKey: string): Promise<YahooTeam> {
    return this.request(`/team/${teamKey}`);
  }

  async getLeague(): Promise<YahooLeague> {
    return this.request(`/league/${LEAGUE_ID}`);
  }

  async getRoster(teamKey: string) {
    return this.request(`/team/${teamKey}/roster`);
  }

  async getTransactions() {
    return this.request(`/league/${LEAGUE_ID}/transactions`);
  }

  async getCurrentTeam() {
    const data = await this.request('/users;use_login=1/games/mlb/teams');
    const team = data.users[0].user.games[0].game.teams[0].team;
    return team;
  }
}

export const yahooService = new YahooFantasyService();