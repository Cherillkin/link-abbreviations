import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  Navigate,
} from "react-router-dom";
import { useContext } from "react";

import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import SignUp from "./pages/SignUp";
import SignIn from "./pages/SignIn";
import AdminDashboard from "./components/AdminDashboard";
import { AuthContext, AuthProvider } from "./context/AuthContext";
import OAuthSuccess from "./components/OAuthSuccess";

function AppContent() {
  const { isAuthenticated, loading, user } = useContext(AuthContext);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        Загрузка...
      </div>
    );
  }

  return (
    <>
      {isAuthenticated && <Navbar />}
      <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
        <Routes>
          <Route
            path="/sign-up"
            element={isAuthenticated ? <Navigate to="/" replace /> : <SignUp />}
          />
          <Route
            path="/sign-in"
            element={isAuthenticated ? <Navigate to="/" replace /> : <SignIn />}
          />
          <Route
            path="/"
            element={
              isAuthenticated ? <Home /> : <Navigate to="/sign-in" replace />
            }
          />
          <Route
            path="/admin"
            element={
              isAuthenticated && user?.id_role === 1 ? (
                <AdminDashboard />
              ) : (
                <Navigate to="/" replace />
              )
            }
          />
          <Route
            path="*"
            element={
              <div>
                Страница не найдена. Перейдите на <Link to="/">главную</Link>
              </div>
            }
          />
          <Route
            path="/oauth-success"
            element={<OAuthSuccess baseUrl="http://127.0.0.1:8000" />}
          />
        </Routes>
      </div>
    </>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  );
}
