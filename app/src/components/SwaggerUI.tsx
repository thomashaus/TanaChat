export function SwaggerUI() {
  return (
    <div className="min-h-screen bg-tana-bg flex flex-col">
      <div className="bg-tana-card border-b border-tana-border px-6 py-4 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
            <span className="text-white font-bold text-sm">TC</span>
          </div>
          <h1 className="text-white font-bold text-lg">API Documentation</h1>
        </div>
        <a href="/" className="text-sm text-tana-muted hover:text-white transition-colors">
          Back to Home
        </a>
      </div>
      <div className="flex-grow relative">
        <iframe
          src="http://localhost:8000/docs"
          className="absolute inset-0 w-full h-full bg-white"
          title="Swagger UI"
        />
      </div>
    </div>
  );
}
