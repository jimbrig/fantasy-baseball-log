import axios from 'axios';

// API base URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// Yahoo API endpoints
const YAHOO_API = {
  initialize: `${API_BASE_URL}/yahoo/initialize`,
  teams: `${API_BASE_URL}/yahoo/teams`,
  standings: `${API_BASE_URL}/yahoo/standings`,
  draft: `${API_BASE_URL}/yahoo/draft`,
  roster: (teamKey: string) => `${API_BASE_URL}/yahoo/roster/${teamKey}`,
  settings: `${API_BASE_URL}/yahoo/settings`,
  collectData: `${API_BASE_URL}/yahoo/collect-data`,
};

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Yahoo service
export const yahooService = {
  /**
   * Initialize Yahoo Fantasy API connection
   */
  initialize: async () => {
    try {
      const response = await apiClient.get(YAHOO_API.initialize);
      return response.data;
    } catch (error) {
      console.error('Error initializing Yahoo API:', error);
      throw error;
    }
  },

  /**
   * Get all teams in the league
   */
  getTeams: async () => {
    try {
      const response = await apiClient.get(YAHOO_API.teams);
      return response.data;
    } catch (error) {
      console.error('Error getting teams:', error);
      throw error;
    }
  },

  /**
   * Get current standings
   */
  getStandings: async () => {
    try {
      const response = await apiClient.get(YAHOO_API.standings);
      return response.data;
    } catch (error) {
      console.error('Error getting standings:', error);
      throw error;
    }
  },

  /**
   * Get draft results
   */
  getDraftResults: async () => {
    try {
      const response = await apiClient.get(YAHOO_API.draft);
      return response.data;
    } catch (error) {
      console.error('Error getting draft results:', error);
      throw error;
    }
  },

  /**
   * Get roster for a team
   */
  getRoster: async (teamKey: string) => {
    try {
      const response = await apiClient.get(YAHOO_API.roster(teamKey));
      return response.data;
    } catch (error) {
      console.error(`Error getting roster for team ${teamKey}:`, error);
      throw error;
    }
  },

  /**
   * Get league settings
   */
  getLeagueSettings: async () => {
    try {
      const response = await apiClient.get(YAHOO_API.settings);
      return response.data;
    } catch (error) {
      console.error('Error getting league settings:', error);
      throw error;
    }
  },

  /**
   * Collect all data from Yahoo Fantasy API
   */
  collectData: async () => {
    try {
      const response = await apiClient.post(YAHOO_API.collectData);
      return response.data;
    } catch (error) {
      console.error('Error collecting data:', error);
      throw error;
    }
  },
};

export default yahooService;
