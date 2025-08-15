import { createContext, useState, useEffect } from "react";
import axios from "axios";
import * as jwt_decode from "jwt-decode";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = document.cookie
      .split("; ")
      .find((row) => row.startsWith("access_token="))
      ?.split("=")[1];

    if (token) {
      const decoded = jwt_decode.default(token);
      setUser({ email: decoded.email, id_role: decoded.id_role });
      setIsAuthenticated(true);
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    const res = await axios.post(
      "http://localhost:8000/auth/sign-in",
      { email, password },
      { withCredentials: true }
    );

    setIsAuthenticated(true);
    setUser({ email, id_role: res.data.id_role });
  };

  const logout = async () => {
    await axios.post(
      "http://localhost:8000/auth/logout",
      {},
      { withCredentials: true }
    );
    setIsAuthenticated(false);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{ isAuthenticated, user, login, logout, loading }}
    >
      {children}
    </AuthContext.Provider>
  );
}
