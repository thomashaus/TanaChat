import { useState, useEffect } from 'react';

export function Homepage() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-tana-bg text-tana-text selection:bg-indigo-500/30 overflow-x-hidden">
      {/* Background Effects */}
      {/* Background Effects Removed for Global Graph */}

      {/* Navigation */}
      <nav
        className={`fixed top-0 w-full z-50 transition-all duration-300 ${scrolled ? 'bg-tana-bg/80 backdrop-blur-md border-b border-tana-border' : 'bg-transparent'}`}
      >
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <span className="text-white font-bold text-sm">TC</span>
            </div>
            <span className="font-bold text-lg tracking-tight">
              TanaChat<span className="text-tana-muted">.ai</span>
            </span>
          </div>

          <div className="hidden md:flex items-center space-x-8">
            <a
              href="https://tana.inc"
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm font-medium text-tana-muted hover:text-white transition-colors"
            >
              Tana
            </a>
            <a
              href="https://claude.ai"
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm font-medium text-tana-muted hover:text-white transition-colors"
            >
              Claude
            </a>
            <a
              href="https://chat.openai.com"
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm font-medium text-tana-muted hover:text-white transition-colors"
            >
              ChatGPT
            </a>
            <a
              href="/signin"
              className="px-4 py-2 rounded-full bg-white text-black text-sm font-semibold hover:bg-gray-200 transition-colors"
            >
              Sign In
            </a>
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden">
            <button onClick={() => setMobileMenuOpen(!mobileMenuOpen)} className="text-white p-2">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                {mobileMenuOpen ? (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                ) : (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Menu Overlay */}
        {mobileMenuOpen && (
          <div className="md:hidden absolute top-16 left-0 w-full bg-tana-bg/95 backdrop-blur-xl border-b border-tana-border p-6 flex flex-col space-y-4 animate-fade-in">
            <a href="https://tana.inc" className="text-lg font-medium text-white">
              Tana
            </a>
            <a href="https://claude.ai" className="text-lg font-medium text-white">
              Claude
            </a>
            <a href="https://chat.openai.com" className="text-lg font-medium text-white">
              ChatGPT
            </a>
            <a
              href="/signin"
              className="px-4 py-3 rounded-xl bg-white text-black text-center font-bold"
            >
              Sign In
            </a>
          </div>
        )}
      </nav>

      {/* Hero Section */}
      <main className="relative z-10 pt-32 pb-20 px-6">
        <div className="max-w-5xl mx-auto text-center">
          <div className="inline-flex items-center px-3 py-1 rounded-full border border-tana-border bg-tana-card/50 backdrop-blur-sm mb-8 animate-fade-in">
            <span className="flex h-2 w-2 rounded-full bg-green-500 mr-2 animate-pulse"></span>
            <span className="text-xs font-medium text-tana-muted">v2.0 Now Available</span>
          </div>

          <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-8 animate-slide-up">
            <span className="bg-clip-text text-transparent bg-gradient-to-b from-white to-white/60">
              The Bridge Between
            </span>
            <br />
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400">
              Tana & AI Intelligence
            </span>
          </h1>

          <p
            className="text-xl text-tana-muted max-w-2xl mx-auto mb-12 leading-relaxed animate-slide-up"
            style={{ animationDelay: '0.1s' }}
          >
            Transform your visual thinking into actionable workflows. Seamlessly connect Tana's
            knowledge graph with the power of Claude and ChatGPT.
          </p>

          <div
            className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4 animate-slide-up"
            style={{ animationDelay: '0.2s' }}
          >
            <a
              href="/chat"
              className="w-full sm:w-auto px-8 py-4 rounded-full bg-white text-black font-bold text-lg hover:bg-gray-200 transition-all transform hover:scale-105 shadow-[0_0_40px_-10px_rgba(255,255,255,0.3)]"
            >
              Get Started
            </a>
            <a
              href={`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/docs`}
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto px-8 py-4 rounded-full border border-tana-border bg-tana-card/30 hover:bg-tana-card/50 text-white font-medium text-lg transition-all backdrop-blur-sm"
            >
              API Documentation
            </a>
          </div>
        </div>

        {/* Feature Grid (Bento Box) */}
        <div
          className="max-w-6xl mx-auto mt-32 grid grid-cols-1 md:grid-cols-3 gap-6 animate-slide-up"
          style={{ animationDelay: '0.4s' }}
        >
          {/* Main Feature */}
          <div className="md:col-span-2 row-span-2 rounded-3xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8 relative overflow-hidden group hover:border-indigo-500/50 transition-colors">
            <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/10 to-purple-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
            <h3 className="text-2xl font-bold mb-4">Visual Knowledge Graph</h3>
            <p className="text-tana-muted mb-8 max-w-md">
              Your thoughts aren't linear, and neither should your AI be. TanaChat respects the
              structure of your Tana workspace while injecting AI capabilities exactly where you
              need them.
            </p>
            <div className="absolute bottom-0 right-0 w-3/4 h-3/4 bg-gradient-to-tl from-tana-border to-transparent rounded-tl-3xl opacity-20" />
          </div>

          {/* Secondary Feature 1 */}
          <div className="rounded-3xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8 relative overflow-hidden group hover:border-orange-500/50 transition-colors">
            <div className="w-12 h-12 rounded-xl bg-orange-500/20 flex items-center justify-center mb-6 text-orange-500">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
            </div>
            <h3 className="text-xl font-bold mb-2">Claude Integration</h3>
            <p className="text-sm text-tana-muted">
              Deep integration with Claude Desktop for advanced reasoning and coding tasks.
            </p>
          </div>

          {/* Secondary Feature 2 */}
          <div className="rounded-3xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8 relative overflow-hidden group hover:border-green-500/50 transition-colors">
            <div className="w-12 h-12 rounded-xl bg-green-500/20 flex items-center justify-center mb-6 text-green-500">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <h3 className="text-xl font-bold mb-2">ChatGPT Connect</h3>
            <p className="text-sm text-tana-muted">
              Seamlessly pipe data to and from ChatGPT for creative writing and brainstorming.
            </p>
          </div>
        </div>
      </main>

      {/* CLI Power Section */}
      <section className="py-24 px-6 relative z-10">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col lg:flex-row items-center gap-12">
            <div className="lg:w-1/2">
              <h2 className="text-4xl font-bold mb-6">
                <span className="bg-clip-text text-transparent bg-gradient-to-r from-green-400 to-emerald-600">
                  Command Line Power
                </span>
              </h2>
              <p className="text-xl text-tana-muted mb-8 leading-relaxed">
                For power users, TanaChat offers a robust suite of CLI tools. Automate your
                workflow, batch process files, and integrate with your existing dev environment.
              </p>
              <ul className="space-y-4 mb-8">
                {[
                  'Batch import JSON exports',
                  'Generate Obsidian vaults',
                  'Analyze workspace structure',
                  'Scriptable via Python API',
                ].map((item, i) => (
                  <li key={i} className="flex items-center text-gray-300">
                    <svg
                      className="w-5 h-5 text-green-500 mr-3"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M5 13l4 4L19 7"
                      />
                    </svg>
                    {item}
                  </li>
                ))}
              </ul>
              <a
                href="/hub"
                className="inline-flex items-center text-green-400 font-semibold hover:text-green-300 transition-colors"
              >
                Explore CLI Tools <span className="ml-2">→</span>
              </a>
            </div>

            <div className="lg:w-1/2 w-full">
              <div className="rounded-xl overflow-hidden bg-[#1e1e1e] border border-gray-800 shadow-2xl font-mono text-sm">
                <div className="bg-[#2d2d2d] px-4 py-2 flex items-center space-x-2 border-b border-gray-800">
                  <div className="w-3 h-3 rounded-full bg-red-500"></div>
                  <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                  <div className="w-3 h-3 rounded-full bg-green-500"></div>
                  <div className="ml-4 text-gray-400 text-xs">user@tanachat:~/workspace</div>
                </div>
                <div className="p-6 space-y-2">
                  <div className="flex">
                    <span className="text-green-400 mr-2">➜</span>
                    <span className="text-blue-400 mr-2">~</span>
                    <span className="text-gray-300">
                      ./bin/tana-analyze --export workspace.json
                    </span>
                  </div>
                  <div className="text-gray-400 pl-4">
                    <div>Analyzing workspace structure...</div>
                    <div className="text-green-500">✓ Found 1,243 nodes</div>
                    <div className="text-green-500">✓ Identified 15 supertags</div>
                    <div className="mt-2">Generating report:</div>
                    <div className="pl-4 border-l-2 border-gray-700 mt-1">
                      <div>- Projects: 12 active</div>
                      <div>- Tasks: 45 pending</div>
                      <div>- Notes: 892 archived</div>
                    </div>
                  </div>
                  <div className="flex mt-4">
                    <span className="text-green-400 mr-2">➜</span>
                    <span className="text-blue-400 mr-2">~</span>
                    <span className="animate-pulse">_</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Standard Footer */}
      <footer className="border-t border-tana-border py-12 px-6 bg-tana-bg relative z-10">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between">
          <div className="flex items-center space-x-2 mb-4 md:mb-0">
            <div className="w-6 h-6 rounded bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
              <span className="text-white font-bold text-xs">TC</span>
            </div>
            <span className="font-semibold text-tana-muted">TanaChat.ai</span>
          </div>
          <div className="flex space-x-6 text-sm text-tana-muted">
            <a href="/privacy" className="hover:text-white transition-colors">
              Privacy
            </a>
            <a href="/terms" className="hover:text-white transition-colors">
              Terms
            </a>
            <a
              href="https://github.com/thomashaus/TanaChat"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-white transition-colors"
            >
              GitHub
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
