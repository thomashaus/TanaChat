import { useState, useRef, useEffect, FormEvent } from 'react';

interface Message {
  id: string;
  role: 'user' | 'ai';
  content: string;
  nodes?: TanaNode[];
}

interface TanaNode {
  id: string;
  title: string;
  tag: string;
  fields: { key: string; value: string }[];
}

export function ChatInterface() {
  const [input, setInput] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'ai',
      content: "Hello! I'm connected to your Tana workspace. How can I help you today?",
    },
  ]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isThinking]);

  const handleSend = (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setIsThinking(true);

    // Simulate AI processing
    setTimeout(() => {
      setIsThinking(false);
      const aiMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'ai',
        content: 'I found some relevant nodes in your workspace based on that request:',
        nodes: [
          {
            id: 'node-1',
            title: 'Project: TanaChat Launch',
            tag: '#project',
            fields: [
              { key: 'Status', value: 'In Progress' },
              { key: 'Due Date', value: 'Dec 25, 2024' },
            ],
          },
        ],
      };
      setMessages((prev) => [...prev, aiMsg]);
    }, 2000);
  };

  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen bg-tana-bg overflow-hidden relative">
      {/* Mobile Sidebar Overlay */}
      {mobileSidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 md:hidden"
          onClick={() => setMobileSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div
        className={`fixed md:relative z-50 w-64 bg-tana-card/30 border-r border-tana-border flex flex-col h-full transition-transform duration-300 transform ${mobileSidebarOpen ? 'translate-x-0' : '-translate-x-full'} md:translate-x-0 bg-tana-bg md:bg-transparent`}
      >
        <div className="p-4 border-b border-tana-border flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
              <span className="text-white font-bold text-sm">TC</span>
            </div>
            <span className="font-bold text-white">TanaChat</span>
          </div>
          <button onClick={() => setMobileSidebarOpen(false)} className="md:hidden text-gray-400">
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

        <div className="flex-1 overflow-y-auto p-4 space-y-2">
          <div className="text-xs font-semibold text-tana-muted uppercase mb-2">Recent Threads</div>
          {['Project Planning', 'Meeting Notes Analysis', 'Content Ideas'].map((thread, i) => (
            <button
              key={i}
              className="w-full text-left px-3 py-2 rounded-lg text-sm text-gray-300 hover:bg-white/5 hover:text-white transition-colors truncate"
            >
              {thread}
            </button>
          ))}
        </div>

        <div className="p-4 border-t border-tana-border">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-xs font-bold text-white">
              JD
            </div>
            <div className="text-sm">
              <div className="text-white font-medium">John Doe</div>
              <div className="text-tana-muted text-xs">Pro Plan</div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col relative w-full">
        {/* Header */}
        <div className="h-16 border-b border-tana-border flex items-center justify-between px-4 md:px-6 bg-tana-bg/80 backdrop-blur-md z-10">
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setMobileSidebarOpen(true)}
              className="md:hidden text-gray-400 mr-2"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
            </button>
            <span className="text-tana-muted hidden sm:inline">Context:</span>
            <span className="px-2 py-1 rounded-md bg-indigo-500/20 text-indigo-400 text-xs font-medium border border-indigo-500/30 truncate max-w-[150px] sm:max-w-none">
              Entire Workspace
            </span>
          </div>
          <div className="flex items-center space-x-4">
            <a href="/" className="text-tana-muted hover:text-white transition-colors">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </a>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6 scroll-smooth">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-2xl ${msg.role === 'user' ? 'bg-indigo-600 text-white' : 'bg-tana-card border border-tana-border text-gray-200'} rounded-2xl px-6 py-4 shadow-lg`}
              >
                <p className="leading-relaxed">{msg.content}</p>

                {/* Tana Node Visualization */}
                {msg.nodes && (
                  <div className="mt-4 space-y-3">
                    {msg.nodes.map((node) => (
                      <div
                        key={node.id}
                        className="bg-black/40 rounded-xl p-4 border border-tana-border hover:border-indigo-500/50 transition-colors cursor-pointer group"
                      >
                        <div className="flex items-center space-x-2 mb-3">
                          <span className="w-2 h-2 rounded-full bg-yellow-500"></span>
                          <span className="font-bold text-white group-hover:text-indigo-400 transition-colors">
                            {node.title}
                          </span>
                          <span className="px-2 py-0.5 rounded-full bg-gray-700 text-gray-300 text-[10px] font-medium tracking-wide">
                            {node.tag}
                          </span>
                        </div>
                        <div className="space-y-1 pl-4 border-l-2 border-gray-700">
                          {node.fields.map((field, i) => (
                            <div key={i} className="text-sm flex">
                              <span className="text-tana-muted w-24">{field.key}:</span>
                              <span className="text-gray-300">{field.value}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {isThinking && (
            <div className="flex justify-start">
              <div className="bg-tana-card border border-tana-border rounded-2xl px-6 py-4 shadow-lg flex items-center space-x-2">
                <div
                  className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce"
                  style={{ animationDelay: '0s' }}
                ></div>
                <div
                  className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce"
                  style={{ animationDelay: '0.2s' }}
                ></div>
                <div
                  className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce"
                  style={{ animationDelay: '0.4s' }}
                ></div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-6 bg-gradient-to-t from-tana-bg via-tana-bg to-transparent">
          <form onSubmit={handleSend} className="max-w-4xl mx-auto relative">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask anything about your Tana workspace..."
              className="w-full bg-tana-card/80 backdrop-blur-xl border border-tana-border rounded-2xl pl-6 pr-32 py-4 text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 shadow-2xl transition-all"
            />
            <div className="absolute right-3 top-1/2 transform -translate-y-1/2 flex items-center space-x-2">
              <button
                type="button"
                className="p-2 text-gray-400 hover:text-white transition-colors"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"
                  />
                </svg>
              </button>
              <button
                type="submit"
                disabled={!input.trim() || isThinking}
                className="p-2 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M5 10l7-7m0 0l7 7m-7-7v18"
                  />
                </svg>
              </button>
            </div>
          </form>
          <div className="text-center mt-2">
            <p className="text-[10px] text-tana-muted">
              AI can make mistakes. Please verify important information.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
