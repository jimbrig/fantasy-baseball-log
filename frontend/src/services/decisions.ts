import axios from 'axios';
import { Decision, DecisionCreate, DecisionUpdate, DecisionType } from '../types';

// API base URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

// Decision API endpoints
const DECISIONS_API = {
  base: `${API_BASE_URL}/decisions`,
  byId: (id: string) => `${API_BASE_URL}/decisions/${id}`,
};

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Decision service
export const decisionService = {
  /**
   * Get all decisions with optional filtering
   */
  getDecisions: async (
    page = 1,
    limit = 10,
    type?: DecisionType
  ): Promise<{ items: Decision[]; total: number }> => {
    try {
      const skip = (page - 1) * limit;
      const params: Record<string, string | number> = { skip, limit };

      if (type) {
        params.decision_type = type;
      }

      const response = await apiClient.get(DECISIONS_API.base, { params });
      return response.data;
    } catch (error) {
      console.error('Error getting decisions:', error);
      throw error;
    }
  },

  /**
   * Get a decision by ID
   */
  getDecision: async (id: string): Promise<Decision> => {
    try {
      const response = await apiClient.get(DECISIONS_API.byId(id));
      return response.data;
    } catch (error) {
      console.error(`Error getting decision ${id}:`, error);
      throw error;
    }
  },

  /**
   * Create a new decision
   */
  createDecision: async (decision: DecisionCreate): Promise<Decision> => {
    try {
      const response = await apiClient.post(DECISIONS_API.base, decision);
      return response.data;
    } catch (error) {
      console.error('Error creating decision:', error);
      throw error;
    }
  },

  /**
   * Update an existing decision
   */
  updateDecision: async (id: string, decision: DecisionUpdate): Promise<Decision> => {
    try {
      const response = await apiClient.put(DECISIONS_API.byId(id), decision);
      return response.data;
    } catch (error) {
      console.error(`Error updating decision ${id}:`, error);
      throw error;
    }
  },

  /**
   * Delete a decision
   */
  deleteDecision: async (id: string): Promise<void> => {
    try {
      await apiClient.delete(DECISIONS_API.byId(id));
    } catch (error) {
      console.error(`Error deleting decision ${id}:`, error);
      throw error;
    }
  },
};

export default decisionService;
