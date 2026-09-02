import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';
import ErrorBoundary from './components/ErrorBoundary';

// Pages Modules
import { LandingPage } from './pages/LandingPage';
import { LoginPage, RegisterPage } from './pages/AuthPages';
import { CompetenciesPage, GapAnalysisPage, ProgressPage } from './pages/AnalyticsPages';
import { RecommendationsPage, LearningPathPage, GovernmentHubPage, OnboardingPage } from './pages/LearningPages';
import { StudioPage, QuizPage, AssessmentPage, FinalInterviewPage } from './pages/AssessmentPages';
import { DashboardPage, ProfilePage, AdminPage } from './pages/UserPages';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center text-xs text-[#78716C] font-mono">
        Verifying official session telemetry...
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

const AdminRoute = ({ children }) => {
  const { isAuthenticated, isAdmin, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center text-xs text-[#78716C] font-mono">
        Verifying administrative authorization...
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (!isAdmin) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center space-y-4">
        <div className="p-6 bg-[#FEF2F2] border border-[#FCA5A5] rounded-lg text-[#991B1B]">
          <h2 className="text-lg font-bold">403 Forbidden: Administrative Authorization Required</h2>
          <p className="text-xs mt-1 text-[#78716C]">
            Your officer account does not have administrative privileges required for workforce analytics and system configuration.
          </p>
          <a
            href="/dashboard"
            className="inline-block mt-4 px-4 py-2 bg-[#991B1B] text-white text-xs font-bold rounded hover:bg-[#7F1D1D] transition"
          >
            Return to Learner Dashboard
          </a>
        </div>
      </div>
    );
  }

  return children;
};

const AppLayout = () => {
  const { isAuthenticated } = useAuth();
  const location = useLocation();

  const isPublicRoute = !isAuthenticated || ['/', '/login', '/register'].includes(location.pathname);

  return (
    <div className="min-h-screen flex flex-col bg-[#FAFAF9] text-[#1C1917]">
      <Navbar />
      
      {/* Main Content: Apply lg:pl-64 ONLY for authenticated sidebar routes */}
      <main className={`flex-1 flex flex-col ${isPublicRoute ? 'pl-0' : 'lg:pl-64'}`}>
        <div className="flex-1 pb-10">
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />

            {/* Protected Routes */}
            <Route
              path="/onboarding"
              element={
                <ProtectedRoute>
                  <OnboardingPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <DashboardPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/assessment"
              element={
                <ProtectedRoute>
                  <AssessmentPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/competencies"
              element={
                <ProtectedRoute>
                  <CompetenciesPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/gap-analysis"
              element={
                <ProtectedRoute>
                  <GapAnalysisPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/recommendations"
              element={
                <ProtectedRoute>
                  <RecommendationsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/learning-path"
              element={
                <ProtectedRoute>
                  <LearningPathPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/hub"
              element={
                <ProtectedRoute>
                  <GovernmentHubPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/studio"
              element={
                <ProtectedRoute>
                  <StudioPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/quiz/:id"
              element={
                <ProtectedRoute>
                  <QuizPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/progress"
              element={
                <ProtectedRoute>
                  <ProgressPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <ProfilePage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin"
              element={
                <AdminRoute>
                  <AdminPage />
                </AdminRoute>
              }
            />
            <Route
              path="/final-interview"
              element={
                <ProtectedRoute>
                  <FinalInterviewPage />
                </ProtectedRoute>
              }
            />

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>

        <Footer />
      </main>
    </div>
  );
};

export default function App() {
  return (
    <ErrorBoundary>
      <AuthProvider>
        <Router>
          <AppLayout />
        </Router>
      </AuthProvider>
    </ErrorBoundary>
  );
}
