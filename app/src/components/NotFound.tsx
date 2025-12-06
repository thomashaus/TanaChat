export function NotFound() {
  return (
    <div className="min-h-screen bg-tana-bg flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background Ambience */}
      <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 brightness-100 contrast-150 mix-blend-overlay"></div>
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-indigo-900/20 rounded-full blur-[120px] animate-pulse"></div>

      <div className="text-center relative z-10 animate-fade-in">
        <h1 className="text-9xl font-bold text-white mb-4 opacity-10">404</h1>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-full">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">Node Not Found</h2>
          <p className="text-tana-muted text-lg mb-8 max-w-md mx-auto">
            The knowledge graph path you are looking for seems to be disconnected or doesn't exist.
          </p>
          <a
            href="/"
            className="inline-flex items-center px-6 py-3 border border-tana-border rounded-full bg-tana-card/50 hover:bg-white hover:text-black transition-all duration-300 text-white font-medium group"
          >
            <svg
              className="w-5 h-5 mr-2 transform group-hover:-translate-x-1 transition-transform"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M10 19l-7-7m0 0l7-7m-7 7h18"
              />
            </svg>
            Return to Base
          </a>
        </div>
      </div>

      {/* Floating Elements */}
      <div className="absolute top-1/3 right-1/4 w-4 h-4 bg-indigo-500 rounded-full animate-float opacity-50"></div>
      <div
        className="absolute bottom-1/3 left-1/3 w-3 h-3 bg-purple-500 rounded-full animate-float opacity-30"
        style={{ animationDelay: '-2s' }}
      ></div>
    </div>
  );
}
