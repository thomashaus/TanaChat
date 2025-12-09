import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

interface HeaderProps {
  title?: string;
}

export function Header({ title = 'TanaChat' }: HeaderProps) {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className="bg-tana-card/80 backdrop-blur-lg border-b border-tana-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <h1 className="text-xl font-bold text-white">{title}</h1>
          </div>
          <nav className="hidden md:flex space-x-8">
            <Link
              to="/dashboard"
              className="text-tana-text hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              Dashboard
            </Link>
            <Link
              to="/search"
              className="text-tana-text hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              Search
            </Link>
            <Link
              to="/supertags"
              className="text-tana-text hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              Supertags
            </Link>
            <Link
              to="/mcp"
              className="text-tana-text hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              MCP
            </Link>
            <Link
              to="/users"
              className="text-tana-text hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              Users
            </Link>
            <button
              onClick={handleLogout}
              className="text-tana-text hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              Logout
            </button>
          </nav>
          <div className="md:hidden">
            <div className="flex space-x-2">
              <Link to="/dashboard" className="text-tana-text hover:text-white p-2 rounded-md">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
                  />
                </svg>
              </Link>
              <button
                onClick={handleLogout}
                className="text-tana-text hover:text-white p-2 rounded-md"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
