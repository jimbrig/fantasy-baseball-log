import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

// Pages (to be implemented)
const Dashboard = () => <div>Dashboard Page</div>;
const DecisionLog = () => <div>Decision Log Page</div>;
const DecisionDetail = () => <div>Decision Detail Page</div>;
const CreateDecision = () => <div>Create Decision Page</div>;
const TeamAnalysis = () => <div>Team Analysis Page</div>;
const WaiverAnalysis = () => <div>Waiver Analysis Page</div>;

// Components (to be implemented)
const Header = ({ teamName, onLogout }: { teamName: string; onLogout: () => void }) => (
  <header className="bg-blue-600 text-white p-4">
    <div className="container mx-auto flex justify-between items-center">
      <h1 className="text-xl font-bold">{teamName}</h1>
      <button onClick={onLogout} className="bg-blue-700 px-4 py-2 rounded hover:bg-blue-800">
        Logout
      </button>
    </div>
  </header>
);

const Sidebar = () => (
  <aside className="bg-gray-100 w-64 p-4 h-full">
    <nav>
      <ul className="space-y-2">
        <li>
          <a href="/" className="block p-2 hover:bg-gray-200 rounded">
            Dashboard
          </a>
        </li>
        <li>
          <a href="/decisions" className="block p-2 hover:bg-gray-200 rounded">
            Decision Log
          </a>
        </li>
        <li>
          <a href="/team-analysis" className="block p-2 hover:bg-gray-200 rounded">
            Team Analysis
          </a>
        </li>
        <li>
          <a href="/waiver-analysis" className="block p-2 hover:bg-gray-200 rounded">
            Waiver Analysis
          </a>
        </li>
      </ul>
    </nav>
  </aside>
);

// Login Page
const Login = () => {
  const handleLogin = () => {
    // Implement Yahoo OAuth login
    console.log('Login clicked');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-96">
        <h1 className="text-2xl font-bold mb-6 text-center">Fantasy Baseball Decision Log</h1>
        <p className="mb-6 text-gray-600 text-center">
          Track and analyze your fantasy baseball decisions throughout the season.
        </p>
        <button
          onClick={handleLogin}
          className="w-full bg-purple-600 text-white py-2 px-4 rounded hover:bg-purple-700"
        >
          Login with Yahoo Fantasy
        </button>
      </div>
    </div>
  );
};

// Create Query Client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
    },
  },
});

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleLogout = () => {
    setIsAuthenticated(false);
  };

  if (!isAuthenticated) {
    return <Login />;
  }

  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Header teamName="Fantasy Baseball Dashboard" onLogout={handleLogout} />
          <div className="flex min-h-[calc(100vh-64px)]">
            <Sidebar />
            <main className="flex-1 p-6 overflow-y-auto">
              {error && (
                <div className="mb-4 p-4 bg-red-100 border border-red-200 rounded text-red-700">
                  {error}
                </div>
              )}
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/decisions" element={<DecisionLog />} />
                <Route path="/decisions/:id" element={<DecisionDetail />} />
                <Route path="/decisions/create" element={<CreateDecision />} />
                <Route path="/team-analysis" element={<TeamAnalysis />} />
                <Route path="/waiver-analysis" element={<WaiverAnalysis />} />
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </main>
          </div>
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
