import { useState } from 'react';

export function DocumentationHub() {
  const [activeSection, setActiveSection] = useState('overview');

  const sections = [
    {
      id: 'overview',
      title: 'Overview',
      icon: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
    },
    {
      id: 'architecture',
      title: 'Architecture',
      icon: 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10',
    },
    {
      id: 'cli-tools',
      title: 'CLI Tools',
      icon: 'M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z',
    },
    { id: 'api-ref', title: 'API Reference', icon: 'M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4' },
  ];

  return (
    <div className="min-h-screen bg-tana-bg flex">
      {/* Sidebar */}
      <div className="w-64 border-r border-tana-border bg-tana-card/30 backdrop-blur-md fixed h-full z-20 hidden md:block">
        <div className="p-6">
          <div className="flex items-center space-x-2 mb-8">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
              <span className="text-white font-bold text-sm">TC</span>
            </div>
            <span className="font-bold text-white">Docs Hub</span>
          </div>

          <nav className="space-y-2">
            {sections.map((section) => (
              <button
                key={section.id}
                onClick={() => setActiveSection(section.id)}
                className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                  activeSection === section.id
                    ? 'bg-indigo-500/20 text-indigo-400 border border-indigo-500/30'
                    : 'text-tana-muted hover:bg-white/5 hover:text-white'
                }`}
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d={section.icon}
                  />
                </svg>
                <span className="font-medium">{section.title}</span>
              </button>
            ))}
          </nav>
        </div>

        <div className="absolute bottom-0 w-full p-6 border-t border-tana-border">
          <a
            href="/"
            className="flex items-center text-sm text-tana-muted hover:text-white transition-colors"
          >
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M10 19l-7-7m0 0l7-7m-7 7h18"
              />
            </svg>
            Back to App
          </a>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 md:ml-64 p-8 md:p-12 overflow-y-auto">
        <div className="max-w-4xl mx-auto animate-fade-in">
          <div className="mb-12">
            <h1 className="text-4xl font-bold text-white mb-4">Documentation Hub</h1>
            <p className="text-xl text-tana-muted">Everything you need to build with TanaChat.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Mock Content Cards */}
            <div className="bg-tana-card border border-tana-border rounded-2xl p-6 hover:border-indigo-500/50 transition-colors group cursor-pointer">
              <div className="w-12 h-12 rounded-xl bg-blue-500/20 flex items-center justify-center mb-4 text-blue-400 group-hover:scale-110 transition-transform">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
                  />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-2">System Architecture</h3>
              <p className="text-tana-muted mb-4">
                Deep dive into the core components: API, Validator, and MCP Server.
              </p>
              <span className="text-indigo-400 text-sm font-medium group-hover:underline">
                Read more →
              </span>
            </div>

            <div className="bg-tana-card border border-tana-border rounded-2xl p-6 hover:border-green-500/50 transition-colors group cursor-pointer">
              <div className="w-12 h-12 rounded-xl bg-green-500/20 flex items-center justify-center mb-4 text-green-400 group-hover:scale-110 transition-transform">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-2">CLI Reference</h3>
              <p className="text-tana-muted mb-4">
                Master the command line tools for batch processing and automation.
              </p>
              <span className="text-green-400 text-sm font-medium group-hover:underline">
                View commands →
              </span>
            </div>

            <div className="bg-tana-card border border-tana-border rounded-2xl p-6 hover:border-purple-500/50 transition-colors group cursor-pointer">
              <div className="w-12 h-12 rounded-xl bg-purple-500/20 flex items-center justify-center mb-4 text-purple-400 group-hover:scale-110 transition-transform">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M13 10V3L4 14h7v7l9-11h-7z"
                  />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Quick Start Guide</h3>
              <p className="text-tana-muted mb-4">
                Get up and running with TanaChat in less than 5 minutes.
              </p>
              <span className="text-purple-400 text-sm font-medium group-hover:underline">
                Start now →
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
