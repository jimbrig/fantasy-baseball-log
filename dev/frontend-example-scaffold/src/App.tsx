import React, { useEffect, useState } from 'react';
import { Baseline as Baseball } from 'lucide-react';
import { useQuery } from 'react-query';
import DecisionLog from './components/DecisionLog';
import { YahooAuth } from './components/YahooAuth';
import { yahooService } from './services/yahoo';
import type { YahooTeam } from './types';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { data: team, isError } = useQuery<YahooTeam>(
    'currentTeam',
    () => yahooService.getCurrentTeam(),
    {
      enabled: isAuthenticated,
      onError: (err) => {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError('Failed to fetch team data');
        }
        setIsAuthenticated(false);
        yahooService.clearAccessToken();
      },
    }
  );

  useEffect(() => {
    // Check for existing token
    const token = yahooService.getAccessToken();
    if (token) {
      setIsAuthenticated(true);
    }

    // Check for OAuth token in URL hash after redirect
    const hash = window.location.hash;
    if (hash) {
      const token = new URLSearchParams(hash.substring(1)).get('access_token');
      if (token) {
        yahooService.setAccessToken(token);
        setIsAuthenticated(true);
        window.history.replaceState({}, document.title, window.location.pathname);
      }
    }
  }, []);

  const handleLogout = () => {
    yahooService.clearAccessToken();
    setIsAuthenticated(false);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Baseball className="w-8 h-8 text-blue-600 mr-3" />
              <h1 className="text-2xl font-bold text-gray-900">Fantasy Baseball Dashboard</h1>
            </div>
            {isAuthenticated && (
              <button
                onClick={handleLogout}
                className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900"
              >
                Logout
              </button>
            )}
          </div>
          {team && (
            <div className="mt-2 text-sm text-gray-600">
              Connected to: {team.name}
            </div>
          )}
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            {error}
          </div>
        )}
        {!isAuthenticated ? (
          <YahooAuth />
        ) : (
          <DecisionLog />
        )}
      </main>
    </div>
  );
}

export default App;