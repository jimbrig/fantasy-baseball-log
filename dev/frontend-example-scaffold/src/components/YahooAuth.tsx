import React from 'react';
import { LogIn } from 'lucide-react';

const YAHOO_CLIENT_ID = import.meta.env.VITE_YAHOO_CLIENT_ID;
const REDIRECT_URI = import.meta.env.VITE_REDIRECT_URI;

export const YahooAuth: React.FC = () => {
  const handleLogin = () => {
    const authUrl = new URL('https://api.login.yahoo.com/oauth2/request_auth');
    authUrl.searchParams.append('client_id', YAHOO_CLIENT_ID);
    authUrl.searchParams.append('redirect_uri', REDIRECT_URI);
    authUrl.searchParams.append('response_type', 'token');
    authUrl.searchParams.append('language', 'en-us');
    
    // Open the auth URL in a new window
    const width = 600;
    const height = 600;
    const left = (window.innerWidth - width) / 2;
    const top = (window.innerHeight - height) / 2;
    
    window.open(
      authUrl.toString(),
      'yahoo-auth',
      `width=${width},height=${height},top=${top},left=${left}`
    );

    // Listen for the redirect message
    window.addEventListener('message', (event) => {
      if (event.origin === window.location.origin) {
        const { hash } = new URL(event.data);
        const token = new URLSearchParams(hash.substring(1)).get('access_token');
        if (token) {
          window.location.hash = hash;
          window.location.reload();
        }
      }
    }, { once: true });
  };

  return (
    <div className="flex flex-col items-center justify-center p-8 bg-white rounded-lg shadow-sm">
      <h2 className="text-xl font-semibold mb-4">Connect to Yahoo Fantasy</h2>
      <p className="text-gray-600 mb-6">
        Connect your Yahoo Fantasy account to automatically sync your team data and league information.
      </p>
      <button
        onClick={handleLogin}
        className="flex items-center px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
      >
        <LogIn className="w-5 h-5 mr-2" />
        Connect Yahoo Account
      </button>
    </div>
  );
};