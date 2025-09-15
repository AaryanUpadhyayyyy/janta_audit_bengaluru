import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ProjectProvider } from './contexts/ProjectContext';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import ProjectDetailPage from './components/ProjectDetailPage';
import ProjectTrackingPage from './pages/ProjectTrackingPage';
import Login from './pages/Login';
import ProjectHealthDashboard from './pages/ProjectHealthDashboard';
import './App.css';

// Simple Error Boundary component
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <h1>Something went wrong. Please refresh the page.</h1>;
    }
    return this.props.children;
  }
}

function App() {
  return (
    <ErrorBoundary>
      <AuthProvider>
        <ProjectProvider>
          <Router>
            <div className="App">
              <Navbar />
              <main>
                <Routes>
                  <Route path="/" element={<HomePage />} />
                  <Route path="/projects" element={<ProjectTrackingPage />} />
                  <Route path="/project/:id" element={<ProjectDetailPage />} />
                  <Route path="/login" element={<Login />} />
                  <Route path="/health-dashboard" element={<ProjectHealthDashboard />} />
                </Routes>
              </main>
            </div>
          </Router>
        </ProjectProvider>
      </AuthProvider>
    </ErrorBoundary>
  );
}

export default App;
