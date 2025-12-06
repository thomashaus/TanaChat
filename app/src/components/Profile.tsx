import { useState, ReactNode } from 'react';

export function Profile() {
  const [connections, setConnections] = useState({
    tana: true,
    openai: true,
    claude: false,
  });

  const toggleConnection = (key: keyof typeof connections) => {
    setConnections((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="min-h-screen bg-tana-bg text-tana-text">
      <div className="max-w-4xl mx-auto px-6 py-12">
        {/* Header */}
        <div className="flex items-center space-x-6 mb-12 animate-fade-in">
          <div className="w-24 h-24 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-3xl font-bold text-white shadow-xl">
            JD
          </div>
          <div>
            <h1 className="text-3xl font-bold text-white mb-1">John Doe</h1>
            <p className="text-tana-muted">Pro Member • Joined Dec 2024</p>
          </div>
          <div className="flex-grow"></div>
          <button className="px-4 py-2 border border-tana-border rounded-lg hover:bg-white/5 transition-colors text-sm">
            Edit Profile
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Connected Apps */}
          <div className="bg-tana-card border border-tana-border rounded-2xl p-8 animate-slide-up">
            <h2 className="text-xl font-bold text-white mb-6">Connected Apps</h2>
            <div className="space-y-6">
              <ConnectionItem
                name="Tana"
                description="Sync workspace nodes"
                connected={connections.tana}
                onToggle={() => toggleConnection('tana')}
                icon={
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M13 10V3L4 14h7v7l9-11h-7z"
                  />
                }
                color="text-yellow-400"
              />
              <ConnectionItem
                name="OpenAI"
                description="GPT-4 access"
                connected={connections.openai}
                onToggle={() => toggleConnection('openai')}
                icon={
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                }
                color="text-green-400"
              />
              <ConnectionItem
                name="Claude"
                description="Anthropic API"
                connected={connections.claude}
                onToggle={() => toggleConnection('claude')}
                icon={
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
                  />
                }
                color="text-orange-400"
              />
            </div>
          </div>

          {/* Usage Stats */}
          <div
            className="bg-tana-card border border-tana-border rounded-2xl p-8 animate-slide-up"
            style={{ animationDelay: '0.1s' }}
          >
            <h2 className="text-xl font-bold text-white mb-6">Usage Statistics</h2>
            <div className="space-y-8">
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-tana-muted">API Calls</span>
                  <span className="text-white">8,432 / 10,000</span>
                </div>
                <div className="h-2 bg-black rounded-full overflow-hidden">
                  <div className="h-full bg-indigo-500 w-[84%] rounded-full"></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-tana-muted">Storage Used</span>
                  <span className="text-white">1.2GB / 5GB</span>
                </div>
                <div className="h-2 bg-black rounded-full overflow-hidden">
                  <div className="h-full bg-purple-500 w-[24%] rounded-full"></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-tana-muted">Vector Embeddings</span>
                  <span className="text-white">145,200</span>
                </div>
                <div className="h-2 bg-black rounded-full overflow-hidden">
                  <div className="h-full bg-green-500 w-[65%] rounded-full"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

interface ConnectionItemProps {
  name: string;
  description: string;
  connected: boolean;
  onToggle: () => void;
  icon: ReactNode;
  color: string;
}

function ConnectionItem({
  name,
  description,
  connected,
  onToggle,
  icon,
  color,
}: ConnectionItemProps) {
  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center space-x-4">
        <div
          className={`w-10 h-10 rounded-lg bg-white/5 flex items-center justify-center ${color}`}
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            {icon}
          </svg>
        </div>
        <div>
          <div className="font-medium text-white">{name}</div>
          <div className="text-xs text-tana-muted">{description}</div>
        </div>
      </div>
      <button
        onClick={onToggle}
        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none ${connected ? 'bg-indigo-600' : 'bg-gray-700'}`}
      >
        <span
          className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${connected ? 'translate-x-6' : 'translate-x-1'}`}
        />
      </button>
    </div>
  );
}
