import { useState, useEffect } from 'react';
import { Header } from './Header';
import { Footer } from './Footer';

interface User {
  username: string;
  email: string;
  id?: string;
  created_at?: string;
  last_login?: string;
}

interface ImportResult {
  filename: string;
  size: number;
  uploaded: string;
  nodes: number;
}

export function Dashboard() {
  const [user, setUser] = useState<User | null>(null);
  const [newTanaToken, setNewTanaToken] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string>('');
  const [importFile, setImportFile] = useState<File | null>(null);
  const [importResult, setImportResult] = useState<ImportResult | null>(null);

  useEffect(() => {
    // Get user info from localStorage or token
    const token = localStorage.getItem('authToken');
    const userInfo = localStorage.getItem('userInfo');

    if (token && userInfo) {
      setUser(JSON.parse(userInfo));
    }
  }, []);

  const handleUpdateTanaToken = async () => {
    if (!newTanaToken.trim()) {
      setMessage('Please enter a valid Tana API token');
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      // Store Tana token in localStorage for now
      localStorage.setItem('tanaApiToken', newTanaToken);
      setNewTanaToken('');
      setMessage('Tana API token saved successfully! (stored locally)');
    } catch {
      setMessage('Error saving Tana API token');
    } finally {
      setLoading(false);
    }
  };

  const handleImportTanaJSON = async () => {
    if (!importFile) {
      setMessage('Please select a Tana JSON file');
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      // Read and validate the JSON file locally for now
      const text = await importFile.text();
      const json = JSON.parse(text);

      // Store in localStorage as a demo
      const importData = {
        filename: importFile.name,
        size: importFile.size,
        uploaded: new Date().toISOString(),
        nodes: json.length || Object.keys(json).length,
      };

      localStorage.setItem('lastTanaImport', JSON.stringify(importData));
      setImportResult(importData);
      setMessage(`Successfully processed ${importFile.name} (${importData.size} bytes)`);
      setImportFile(null);
    } catch {
      setMessage('Error reading Tana JSON file - please check the file format');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-tana-bg text-tana-text">
      <Header title="Dashboard" />

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        <h1 className="text-3xl font-bold mb-8">Dashboard</h1>

        {/* Alert Messages */}
        {message && (
          <div
            className={`mb-6 p-4 rounded-lg ${
              message.includes('success')
                ? 'bg-green-500/20 border border-green-500 text-green-300'
                : 'bg-red-500/20 border border-red-500 text-red-300'
            }`}
          >
            {message}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* User Details Component */}
          <div className="bg-tana-card border border-tana-border rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <span className="mr-2">👤</span> User Details
            </h2>
            {user ? (
              <div className="space-y-2 text-sm">
                <div>
                  <strong>Username:</strong> {user.username}
                </div>
                <div>
                  <strong>Email:</strong> {user.email}
                </div>
                <div>
                  <strong>User ID:</strong> {user.id || 'N/A'}
                </div>
                <div>
                  <strong>Created:</strong> {user.created_at || 'N/A'}
                </div>
                <div>
                  <strong>Last Login:</strong> {user.last_login || 'N/A'}
                </div>
              </div>
            ) : (
              <div className="text-tana-muted">User information not available</div>
            )}
          </div>

          {/* Show TanaChat Token Component */}
          <div className="bg-tana-card border border-tana-border rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <span className="mr-2">🔑</span> TanaChat Token
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Current Token</label>
                <div className="p-3 bg-tana-bg rounded font-mono text-xs break-all">
                  {localStorage.getItem('authToken') || 'No token'}
                </div>
              </div>
              <div className="text-xs text-tana-muted">
                <div>
                  <strong>Token Type:</strong> Bearer
                </div>
                <div>
                  <strong>Expires In:</strong> 30 days
                </div>
              </div>
            </div>
          </div>

          {/* Update Tana API Token Component */}
          <div className="bg-tana-card border border-tana-border rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <span className="mr-2">🔄</span> Update Tana API Token
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">New Tana API Token</label>
                <input
                  type="password"
                  value={newTanaToken}
                  onChange={(e) => setNewTanaToken(e.target.value)}
                  placeholder="Enter your new Tana API token"
                  className="w-full p-3 bg-tana-bg border border-tana-border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
              <button
                onClick={handleUpdateTanaToken}
                disabled={loading}
                className="w-full py-3 px-4 bg-indigo-500 text-white rounded-lg hover:bg-indigo-600 disabled:opacity-50 transition-colors"
              >
                {loading ? 'Updating...' : 'Update Tana Token'}
              </button>
            </div>
          </div>

          {/* Import New Tana JSON Component */}
          <div className="bg-tana-card border border-tana-border rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <span className="mr-2">📤</span> Import New Tana JSON
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Select Tana JSON File</label>
                <input
                  type="file"
                  accept=".json"
                  onChange={(e) => setImportFile(e.target.files?.[0] || null)}
                  className="w-full p-3 bg-tana-bg border border-tana-border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
              {importFile && (
                <div className="text-sm text-tana-muted">
                  Selected: {importFile.name} ({(importFile.size / 1024).toFixed(2)} KB)
                </div>
              )}
              <button
                onClick={handleImportTanaJSON}
                disabled={loading || !importFile}
                className="w-full py-3 px-4 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:opacity-50 transition-colors"
              >
                {loading ? 'Importing...' : 'Import Tana JSON'}
              </button>
            </div>
          </div>
        </div>

        {/* Import Results */}
        {importResult && (
          <div className="mt-6 bg-tana-card border border-tana-border rounded-lg p-6">
            <h3 className="text-lg font-semibold mb-4">Import Results</h3>
            <div className="bg-tana-bg p-4 rounded-lg">
              <pre className="text-sm overflow-x-auto">{JSON.stringify(importResult, null, 2)}</pre>
            </div>
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
}
