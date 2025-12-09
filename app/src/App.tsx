import { Routes, Route } from 'react-router-dom';
import { Homepage } from './components/Homepage';
import { HealthDashboard } from './components/HealthDashboard';
import { SwaggerUI } from './components/SwaggerUI';
import { TanaUpload } from './components/TanaUpload';
import { SignIn } from './components/Auth/SignIn';
import { SignUp } from './components/Auth/SignUp';
import { Profile } from './components/Profile';
import { NotFound } from './components/NotFound';
import { DocumentationHub } from './components/DocumentationHub';
import { ChatInterface } from './components/ChatInterface';
import { CommandPalette } from './components/CommandPalette';
import { BackgroundGraph } from './components/BackgroundGraph';
import { Privacy } from './components/Privacy';
import { Terms } from './components/Terms';
import { AuthProvider } from './hooks/useAuth';
import { AuthGuard } from './components/AuthGuard';
import { Dashboard } from './components/Dashboard';
import { Users } from './components/Users';

function App() {
  return (
    <AuthProvider>
      <div className="min-h-screen">
        <BackgroundGraph />
        <CommandPalette />
        <Routes>
          <Route path="/" element={<Homepage />} />
          <Route path="/chat" element={<ChatInterface />} />
          <Route path="/signin" element={<SignIn />} />
          <Route path="/signup" element={<SignUp />} />
          <Route
            path="/dashboard"
            element={
              <AuthGuard>
                <Dashboard />
              </AuthGuard>
            }
          />
          <Route
            path="/users"
            element={
              <AuthGuard>
                <Users />
              </AuthGuard>
            }
          />
          <Route path="/profile" element={<Profile />} />
          <Route path="/health" element={<HealthDashboard />} />
          <Route path="/docs" element={<SwaggerUI />} />
          <Route path="/hub" element={<DocumentationHub />} />
          <Route path="/upload" element={<TanaUpload />} />
          <Route path="/privacy" element={<Privacy />} />
          <Route path="/terms" element={<Terms />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </AuthProvider>
  );
}

export default App;
