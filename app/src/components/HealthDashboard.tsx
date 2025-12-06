import { useState, useEffect } from 'react';

export function HealthDashboard() {
  const [logs, setLogs] = useState<string[]>([
    "[SYSTEM] Initializing health check sequence...",
    "[NETWORK] Connected to Tana API Gateway (v2.1.0)",
    "[AUTH] Secure handshake established with Claude Protocol",
  ]);

  useEffect(() => {
    const interval = setInterval(() => {
      const newLogs = [
        `[${new Date().toLocaleTimeString()}] Heartbeat signal received from worker node`,
        `[${new Date().toLocaleTimeString()}] Syncing knowledge graph delta...`,
        `[${new Date().toLocaleTimeString()}] Optimizing vector embeddings...`,
      ];
      const randomLog = newLogs[Math.floor(Math.random() * newLogs.length)];
      setLogs(prev => [randomLog, ...prev].slice(0, 8));
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-tana-bg text-tana-text p-6 md:p-12 font-mono">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-12">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2 tracking-tight">System Status</h1>
            <p className="text-tana-muted">Real-time operational metrics</p>
          </div>
          <div className="flex items-center space-x-2 px-4 py-2 bg-green-500/10 border border-green-500/20 rounded-full">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
            <span className="text-green-500 text-sm font-bold">ALL SYSTEMS OPERATIONAL</span>
          </div>
        </div>

        {/* Grid Layout */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Status Cards */}
          <StatusCard title="Tana API" status="online" latency="45ms" />
          <StatusCard title="Claude Bridge" status="online" latency="120ms" />
          <StatusCard title="OpenAI Gateway" status="online" latency="89ms" />
          <StatusCard title="Vector DB" status="processing" latency="210ms" />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Metrics Chart (Mock) */}
          <div className="lg:col-span-2 bg-tana-card border border-tana-border rounded-xl p-6 relative overflow-hidden">
            <h3 className="text-lg font-bold text-white mb-6">Resource Usage</h3>
            <div className="flex items-end space-x-2 h-64 w-full">
              {[...Array(40)].map((_, i) => (
                <div
                  key={i}
                  className="flex-1 bg-indigo-500/20 hover:bg-indigo-500/40 transition-colors rounded-t-sm"
                  style={{ height: `${Math.random() * 80 + 20}%` }}
                />
              ))}
            </div>
            <div className="absolute top-0 right-0 p-6 flex space-x-4">
              <div className="text-right">
                <div className="text-xs text-tana-muted">CPU Load</div>
                <div className="text-xl font-bold text-white">42%</div>
              </div>
              <div className="text-right">
                <div className="text-xs text-tana-muted">Memory</div>
                <div className="text-xl font-bold text-white">1.2GB</div>
              </div>
            </div>
          </div>

          {/* Terminal Log */}
          <div className="bg-black border border-tana-border rounded-xl p-6 font-mono text-sm overflow-hidden">
            <div className="flex items-center justify-between mb-4 border-b border-gray-800 pb-2">
              <span className="text-gray-400">Live Logs</span>
              <div className="flex space-x-1.5">
                <div className="w-3 h-3 rounded-full bg-red-500/20"></div>
                <div className="w-3 h-3 rounded-full bg-yellow-500/20"></div>
                <div className="w-3 h-3 rounded-full bg-green-500/20"></div>
              </div>
            </div>
            <div className="space-y-2">
              {logs.map((log, i) => (
                <div key={i} className={`truncate ${i === 0 ? 'text-green-400' : 'text-gray-500'}`}>
                  <span className="opacity-50 mr-2">{">"}</span>
                  {log}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function StatusCard({ title, status, latency }: { title: string, status: 'online' | 'processing' | 'offline', latency: string }) {
  const colors = {
    online: 'bg-green-500',
    processing: 'bg-yellow-500',
    offline: 'bg-red-500'
  };

  return (
    <div className="bg-tana-card border border-tana-border rounded-xl p-6 hover:border-gray-600 transition-colors group">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-gray-200">{title}</h3>
        <div className={`w-2 h-2 rounded-full ${colors[status]} shadow-[0_0_10px_rgba(0,0,0,0.5)]`} style={{ boxShadow: `0 0 10px var(--tw-shadow-color)` }}></div>
      </div>
      <div className="flex items-end justify-between">
        <div className="text-xs text-tana-muted uppercase tracking-wider">Latency</div>
        <div className="text-2xl font-bold text-white group-hover:text-indigo-400 transition-colors">{latency}</div>
      </div>
    </div>
  );
}
