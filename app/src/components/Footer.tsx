import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

interface McpSetupModalProps {
  isOpen: boolean;
  onClose: () => void;
}

function McpSetupModal({ isOpen, onClose }: McpSetupModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="bg-tana-card border border-tana-border rounded-xl p-6 max-w-2xl max-h-[80vh] overflow-y-auto m-4">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-xl font-bold text-white">MCP Server Setup Instructions</h3>
          <button onClick={onClose} className="text-tana-muted hover:text-white transition-colors">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        <div className="space-y-4 text-tana-text">
          <div>
            <h4 className="text-lg font-semibold text-white mb-2">
              Step 1: Install Claude Desktop
            </h4>
            <p>
              Download and install Claude Desktop from{' '}
              <a href="https://claude.ai/download" className="text-blue-400 hover:underline">
                claude.ai/download
              </a>
            </p>
          </div>

          <div>
            <h4 className="text-lg font-semibold text-white mb-2">Step 2: Configure MCP Server</h4>
            <p>Open Claude Desktop settings and add the TanaChat MCP server configuration:</p>
            <div className="bg-black/50 rounded-lg p-4 mt-2">
              <pre className="text-sm text-green-400 overflow-x-auto">
                {`{
  "mcpServers": {
    "tanachat": {
      "command": "python",
      "args": ["-m", "tanachat_mcp.client"],
      "env": {
        "TANACHAT_API_URL": "http://localhost:8000",
        "TANACHAT_API_TOKEN": "your_token_here"
      }
    }
  }
}`}
              </pre>
            </div>
          </div>

          <div>
            <h4 className="text-lg font-semibold text-white mb-2">Step 3: Get Your API Token</h4>
            <p>
              Login to TanaChat and go to your dashboard to get your TanaChat API token. Replace
              "your_token_here" in the configuration above.
            </p>
          </div>

          <div>
            <h4 className="text-lg font-semibold text-white mb-2">
              Step 4: Restart Claude Desktop
            </h4>
            <p>After adding the configuration, restart Claude Desktop to load the MCP server.</p>
          </div>

          <div className="bg-blue-500/20 border border-blue-500/50 rounded-lg p-4">
            <p className="text-blue-300">
              <strong>Note:</strong> The TanaChat MCP server allows you to search and interact with
              your Tana data directly within Claude.
            </p>
          </div>
        </div>

        <div className="mt-6 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
          >
            Got it
          </button>
        </div>
      </div>
    </div>
  );
}

export function Footer() {
  const [showMcpModal, setShowMcpModal] = useState(false);
  const navigate = useNavigate();

  const handleSearchClick = () => {
    navigate('/search');
  };

  const handleSupertagsClick = () => {
    navigate('/supertags');
  };

  const handleMcpSetupClick = () => {
    setShowMcpModal(true);
  };

  return (
    <>
      <footer className="bg-tana-card/80 backdrop-blur-lg border-t border-tana-border mt-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-6">
            <button
              onClick={handleSearchClick}
              className="flex items-center space-x-2 px-4 py-2 bg-tana-bg hover:bg-white/10 rounded-lg transition-colors group"
            >
              <svg
                className="w-5 h-5 text-tana-muted group-hover:text-white transition-colors"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
              <div className="text-left">
                <div className="text-white font-medium">Tanasearch</div>
                <div className="text-xs text-tana-muted">Find in Tana</div>
              </div>
            </button>

            <button
              onClick={handleSupertagsClick}
              className="flex items-center space-x-2 px-4 py-2 bg-tana-bg hover:bg-white/10 rounded-lg transition-colors group"
            >
              <svg
                className="w-5 h-5 text-tana-muted group-hover:text-white transition-colors"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"
                />
              </svg>
              <div className="text-left">
                <div className="text-white font-medium">Supertags</div>
                <div className="text-xs text-tana-muted">Show Supertags list and node count</div>
              </div>
            </button>

            <button
              onClick={handleMcpSetupClick}
              className="flex items-center space-x-2 px-4 py-2 bg-tana-bg hover:bg-white/10 rounded-lg transition-colors group"
            >
              <svg
                className="w-5 h-5 text-tana-muted group-hover:text-white transition-colors"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
                />
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                />
              </svg>
              <div className="text-left">
                <div className="text-white font-medium">MCP Setup</div>
                <div className="text-xs text-tana-muted">Configure MCP server</div>
              </div>
            </button>

            <a
              href="https://github.com/thomashaus/TanaChat/"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center space-x-2 px-4 py-2 bg-tana-bg hover:bg-white/10 rounded-lg transition-colors group"
              title="Get Help"
            >
              <svg
                className="w-5 h-5 text-tana-muted group-hover:text-white transition-colors"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <div className="text-left">
                <div className="text-white font-medium">Help</div>
                <div className="text-xs text-tana-muted">Get support</div>
              </div>
            </a>
          </div>

          <div className="text-center text-tana-muted text-sm mt-6">
            <p>&copy; 2024 TanaChat. All rights reserved.</p>
          </div>
        </div>
      </footer>

      <McpSetupModal isOpen={showMcpModal} onClose={() => setShowMcpModal(false)} />
    </>
  );
}
