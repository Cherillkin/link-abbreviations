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

    const id_role = document.cookie
      .split("; ")
      .find((row) => row.startsWith("id_role="))
      ?.split("=")[1];

    if (token && id_role) {
      try {
        const decoded = jwt_decode.default(token);
        setUser({ email: decoded.email, id_role: parseInt(id_role, 10) });
        setIsAuthenticated(true);
      } catch (err) {
        console.log("Invalid token:", err);
        logout();
      }
    }

    setLoading(false);
  }, []);

  // Обычный логин (email + пароль)
  const loginWithPassword = async (email, password) => {
    const res = await axios.post(
      "http://localhost:8000/auth/sign-in",
      { email, password },
      { withCredentials: true }
    );

    const { access_token, id_role } = res.data;

    setIsAuthenticated(true);
    setUser({ email, id_role });
    document.cookie = `access_token=${access_token}; path=/; max-age=${
      3600 * 24 * 7
    }`;
    document.cookie = `id_role=${id_role}; path=/; max-age=${3600 * 24 * 7}`;
  };

  // OAuth login
  const loginWithOAuth = (token, id_role, email) => {
    setIsAuthenticated(true);
    setUser({ email, id_role });
    document.cookie = `access_token=${token}; path=/; max-age=${3600 * 24 * 7}`;
    document.cookie = `id_role=${id_role}; path=/; max-age=${3600 * 24 * 7}`;
  };

  // Logout
  const logout = async () => {
    try {
      await axios.post(
        "http://localhost:8000/auth/logout",
        {},
        { withCredentials: true }
      );
    } catch (err) {
      console.log("Logout error:", err);
    }

    document.cookie = "access_token=; path=/; max-age=0";
    document.cookie = "id_role=; path=/; max-age=0";

    setIsAuthenticated(false);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        user,
        loading,
        loginWithPassword,
        loginWithOAuth,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}
