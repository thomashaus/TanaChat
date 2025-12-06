import { useState, DragEvent } from 'react';

export function TanaUpload() {
  const [isDragging, setIsDragging] = useState(false);
  const [files, setFiles] = useState<string[]>([]);

  const handleDragOver = (e: DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    // Mock file handling
    setFiles(prev => [...prev, "knowledge-graph-export.json", "notes-backup.md"]);
  };

  return (
    <div className="min-h-screen bg-tana-bg text-tana-text flex items-center justify-center p-6">
      <div className="w-full max-w-2xl">
        <div className="text-center mb-10">
          <h1 className="text-4xl font-bold text-white mb-4 bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-purple-400">
            Upload Knowledge Base
          </h1>
          <p className="text-tana-muted text-lg">
            Drag and drop your Tana exports here to begin the AI indexing process.
          </p>
        </div>

        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`
            relative rounded-3xl border-2 border-dashed transition-all duration-300 p-12 text-center group cursor-pointer
            ${isDragging
              ? 'border-indigo-500 bg-indigo-500/10 scale-[1.02] shadow-[0_0_50px_-10px_rgba(99,102,241,0.3)]'
              : 'border-tana-border bg-tana-card/30 hover:border-gray-500 hover:bg-tana-card/50'
            }
          `}
        >
          <div className="pointer-events-none">
            <div className={`
              w-20 h-20 mx-auto rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center mb-6 shadow-lg transition-transform duration-300
              ${isDragging ? 'scale-110 rotate-3' : 'group-hover:scale-105'}
            `}>
              <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">
              Drop files to upload
            </h3>
            <p className="text-tana-muted">
              or <span className="text-indigo-400 underline">browse</span> from your computer
            </p>
            <p className="text-xs text-gray-500 mt-4">
              Supports .json, .md, .txt (Max 50MB)
            </p>
          </div>
        </div>

        {/* File List */}
        {files.length > 0 && (
          <div className="mt-8 space-y-3 animate-slide-up">
            {files.map((file, i) => (
              <div key={i} className="bg-tana-card border border-tana-border rounded-xl p-4 flex items-center justify-between group hover:border-indigo-500/30 transition-colors">
                <div className="flex items-center space-x-4">
                  <div className="w-10 h-10 rounded-lg bg-gray-800 flex items-center justify-center text-gray-400">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <div>
                    <div className="text-sm font-medium text-white">{file}</div>
                    <div className="text-xs text-tana-muted">Ready to process</div>
                  </div>
                </div>
                <button className="p-2 hover:bg-gray-800 rounded-lg text-gray-400 hover:text-white transition-colors">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            ))}

            <button className="w-full mt-6 py-4 rounded-xl bg-white text-black font-bold text-lg hover:bg-gray-200 transition-all transform hover:scale-[1.02] shadow-lg">
              Process Files
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
