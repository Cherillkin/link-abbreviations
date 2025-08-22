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
import OAuthCallback from "./utils/OAuthCallback";
import RedirectPage from "./components/RedirectPage";
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
            element={
              isAuthenticated ? <Navigate to="/home" replace /> : <SignUp />
            }
          />
          <Route
            path="/sign-in"
            element={
              isAuthenticated ? <Navigate to="/home" replace /> : <SignIn />
            }
          />
          <Route
            path="/home"
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
                <Navigate to="/home" replace />
              )
            }
          />
          <Route path="/r/:code" element={<RedirectPage />} />
          <Route
            path="*"
            element={
              <div>
                Страница не найдена. Перейдите на{" "}
                <Link to="/home" className="text-2xl">
                  главную
                </Link>
              </div>
            }
          />
          <Route path="/oauth-callback" element={<OAuthCallback />} />
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
