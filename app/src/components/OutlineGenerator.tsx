import React, { useState, useCallback } from 'react';

interface OutlineRequest {
  content: string;
  max_depth: number;
  workspace_id?: string;
  start_node?: string;
  format: 'outline' | 'list';
  include_stats: boolean;
}

interface OutlineResponse {
  success: boolean;
  outline: string;
  metadata: {
    max_depth: number;
    workspace_id?: string;
    start_node?: string;
    format: string;
    include_stats: boolean;
    total_nodes: number;
  };
}

export const OutlineGenerator: React.FC = () => {
  const [content, setContent] = useState('');
  const [maxDepth, setMaxDepth] = useState(2);
  const [workspaceId, setWorkspaceId] = useState('');
  const [startNode, setStartNode] = useState('');
  const [format, setFormat] = useState<'outline' | 'list'>('outline');
  const [includeStats, setIncludeStats] = useState(false);
  const [loading, setLoading] = useState(false);
  const [outline, setOutline] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [metadata, setMetadata] = useState<OutlineResponse['metadata'] | null>(null);
  const [validation, setValidation] = useState<any>(null);

  const handleFileUpload = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const text = e.target?.result as string;
        setContent(text);
        // Auto-validate when file is loaded
        validateContent(text);
      };
      reader.readAsText(file);
    }
  }, []);

  const validateContent = useCallback(async (contentToValidate?: string) => {
    const textToValidate = contentToValidate || content;
    if (!textToValidate.trim()) {
      setValidation(null);
      return;
    }

    try {
      const response = await fetch('/api/v1/outline/validate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content: textToValidate }),
      });

      const data = await response.json();
      setValidation(data);
    } catch (err) {
      setValidation(null);
    }
  }, [content]);

  const handleContentChange = useCallback((newContent: string) => {
    setContent(newContent);
    setError(null);
    setOutline(null);
    setMetadata(null);

    // Debounce validation
    const timeoutId = setTimeout(() => {
      validateContent(newContent);
    }, 500);

    return () => clearTimeout(timeoutId);
  }, [validateContent]);

  const generateOutline = useCallback(async () => {
    if (!content.trim()) {
      setError('Please provide Tana JSON content');
      return;
    }

    setLoading(true);
    setError(null);
    setOutline(null);
    setMetadata(null);

    const request: OutlineRequest = {
      content,
      max_depth: maxDepth,
      workspace_id: workspaceId || undefined,
      start_node: startNode || undefined,
      format,
      include_stats: includeStats,
    };

    try {
      const response = await fetch('/api/v1/outline/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      const data: OutlineResponse = await response.json();

      if (data.success) {
        setOutline(data.outline);
        setMetadata(data.metadata);
      } else {
        setError('Failed to generate outline');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  }, [content, maxDepth, workspaceId, startNode, format, includeStats]);

  const downloadOutline = useCallback(() => {
    if (!outline) return;

    const blob = new Blob([outline], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `tana-outline-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }, [outline]);

  return (
    <div className="min-h-screen bg-tana-bg text-tana-text">
      <div className="max-w-6xl mx-auto p-6 space-y-6">
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold text-white bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-purple-400">
            Tana Outline Generator
          </h1>
          <p className="text-tana-muted text-lg">
            Generate hierarchical outlines from your Tana JSON exports
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Input Section */}
          <div className="rounded-3xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
            <h2 className="text-2xl font-bold mb-4 text-white">
              📤 Input Configuration
            </h2>
            <p className="text-tana-muted mb-6">
              Upload a Tana JSON file or paste the content directly
            </p>

            <div className="space-y-6">
              {/* File Upload */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-tana-text">
                  Upload Tana JSON File
                </label>
                <input
                  type="file"
                  accept=".json"
                  onChange={handleFileUpload}
                  className="w-full px-4 py-3 rounded-xl bg-tana-card/50 border border-tana-border text-tana-text placeholder:text-tana-muted focus:outline-none focus:border-indigo-500 focus:bg-tana-card/70 transition-all cursor-pointer"
                />
              </div>

              {/* Content Textarea */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-tana-text">
                  Tana JSON Content
                </label>
                <textarea
                  placeholder="Paste your Tana JSON export content here..."
                  value={content}
                  onChange={(e) => handleContentChange(e.target.value)}
                  className="w-full px-4 py-3 rounded-xl bg-tana-card/50 border border-tana-border text-tana-text placeholder:text-tana-muted focus:outline-none focus:border-indigo-500 focus:bg-tana-card/70 transition-all font-mono text-sm min-h-[200px] resize-none"
                />
                {validation && (
                  <div className={`p-3 rounded-xl border ${
                    validation.valid
                      ? 'border-green-500/30 bg-green-500/10 text-green-400'
                      : 'border-red-500/30 bg-red-500/10 text-red-400'
                  }`}>
                    <p className="text-sm">{validation.message}</p>
                    {validation.stats && (
                      <div className="mt-2 text-sm space-y-1">
                        <div>• Total nodes: {validation.stats.total_nodes}</div>
                        <div>• Root nodes: {validation.stats.root_nodes}</div>
                        <div>• Workspaces: {validation.stats.workspace_count}</div>
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* Configuration Options */}
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-tana-text">
                      Max Depth
                    </label>
                    <input
                      type="number"
                      min="1"
                      max="10"
                      value={maxDepth}
                      onChange={(e) => setMaxDepth(parseInt(e.target.value) || 2)}
                      className="w-full px-4 py-3 rounded-xl bg-tana-card/50 border border-tana-border text-tana-text placeholder:text-tana-muted focus:outline-none focus:border-indigo-500 focus:bg-tana-card/70 transition-all"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-tana-text">
                      Output Format
                    </label>
                    <select
                      value={format}
                      onChange={(e) => setFormat(e.target.value as 'outline' | 'list')}
                      className="w-full px-4 py-3 rounded-xl bg-tana-card/50 border border-tana-border text-tana-text placeholder:text-tana-muted focus:outline-none focus:border-indigo-500 focus:bg-tana-card/70 transition-all"
                    >
                      <option value="outline">Outline</option>
                      <option value="list">List</option>
                    </select>
                  </div>
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium text-tana-text">
                    Workspace ID (Optional)
                  </label>
                  <input
                    type="text"
                    placeholder="Filter by workspace ID"
                    value={workspaceId}
                    onChange={(e) => setWorkspaceId(e.target.value)}
                    className="w-full px-4 py-3 rounded-xl bg-tana-card/50 border border-tana-border text-tana-text placeholder:text-tana-muted focus:outline-none focus:border-indigo-500 focus:bg-tana-card/70 transition-all"
                  />
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium text-tana-text">
                    Start Node ID (Optional)
                  </label>
                  <input
                    type="text"
                    placeholder="Start from specific node"
                    value={startNode}
                    onChange={(e) => setStartNode(e.target.value)}
                    className="w-full px-4 py-3 rounded-xl bg-tana-card/50 border border-tana-border text-tana-text placeholder:text-tana-muted focus:outline-none focus:border-indigo-500 focus:bg-tana-card/70 transition-all"
                  />
                </div>

                <div className="flex items-center space-x-3">
                  <input
                    type="checkbox"
                    id="include-stats"
                    checked={includeStats}
                    onChange={(e) => setIncludeStats(e.target.checked)}
                    className="w-4 h-4 rounded border-tana-border bg-tana-card/50 text-indigo-500 focus:ring-indigo-500 focus:ring-2"
                  />
                  <label htmlFor="include-stats" className="text-sm font-medium text-tana-text">
                    Include Statistics
                  </label>
                </div>
              </div>

              {/* Generate Button */}
              <button
                onClick={generateOutline}
                disabled={loading || !content.trim()}
                className="w-full px-8 py-4 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 text-white font-bold text-lg hover:from-indigo-600 hover:to-purple-600 transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none shadow-[0_0_40px_-10px_rgba(99,102,241,0.3)]"
              >
                {loading ? (
                  <span className="flex items-center justify-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Generating Outline...
                  </span>
                ) : (
                  '👁️ Generate Outline'
                )}
              </button>
            </div>
          </div>

          {/* Output Section */}
          <div className="rounded-3xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-bold text-white">
                📄 Generated Outline
              </h2>
              {outline && (
                <button
                  onClick={downloadOutline}
                  className="px-4 py-2 rounded-xl bg-tana-card/50 border border-tana-border text-tana-text hover:bg-tana-card/70 transition-all text-sm font-medium"
                >
                  Download
                </button>
              )}
            </div>
            <p className="text-tana-muted mb-6">
              Hierarchical view of your Tana workspace structure
            </p>

            {error && (
              <div className="mb-6 p-4 rounded-xl border border-red-500/30 bg-red-500/10 text-red-400">
                <p className="text-sm">{error}</p>
              </div>
            )}

            {metadata && (
              <div className="mb-6 p-4 bg-gray-50 rounded-xl border border-gray-700">
                <h3 className="font-semibold mb-3 text-gray-800">📊 Outline Metadata</h3>
                <div className="grid grid-cols-2 gap-3 text-sm text-gray-600">
                  <div>Format: {metadata.format}</div>
                  <div>Max Depth: {metadata.max_depth}</div>
                  <div>Total Nodes: {metadata.total_nodes.toLocaleString()}</div>
                  <div>Statistics: {metadata.include_stats ? 'Yes' : 'No'}</div>
                  {metadata.workspace_id && (
                    <div className="col-span-2">Workspace: {metadata.workspace_id}</div>
                  )}
                  {metadata.start_node && (
                    <div className="col-span-2">Start Node: {metadata.start_node}</div>
                  )}
                </div>
              </div>
            )}

            {outline ? (
              <div className="bg-gray-900 text-gray-100 p-4 rounded-xl overflow-auto max-h-[600px] border border-gray-700">
                <pre className="text-sm whitespace-pre-wrap font-mono">
                  {outline}
                </pre>
              </div>
            ) : (
              <div className="text-center py-16 text-tana-muted">
                <div className="text-6xl mb-4 opacity-50">📄</div>
                <p>Generate an outline to see the results here</p>
              </div>
            )}
          </div>
        </div>

        {/* Instructions */}
        <div className="rounded-3xl border border-tana-border bg-tana-card/30 backdrop-blur-sm p-8">
          <h3 className="text-xl font-bold mb-4 text-white">How to Use</h3>
          <ol className="list-decimal list-inside space-y-2 text-tana-muted">
            <li>Upload a Tana JSON file or paste the JSON content directly</li>
            <li>Configure the outline options:
              <ul className="list-disc list-inside ml-6 mt-2 text-sm">
                <li><strong>Max Depth:</strong> How many levels to display (1-10)</li>
                <li><strong>Output Format:</strong> Choose between outline or list view</li>
                <li><strong>Workspace ID:</strong> Filter nodes by specific workspace</li>
                <li><strong>Start Node:</strong> Begin from a specific node instead of root</li>
                <li><strong>Include Statistics:</strong> Add detailed statistics about the workspace</li>
              </ul>
            </li>
            <li>Click "Generate Outline" to create the hierarchical view</li>
            <li>Download the outline as a text file for later use</li>
          </ol>
        </div>
      </div>
    </div>
  );
};