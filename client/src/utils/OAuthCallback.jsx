import { useEffect, useContext } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

export default function OAuthCallback() {
  const navigate = useNavigate();
  const location = useLocation();
  const { loginWithOAuth } = useContext(AuthContext);

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const access_token = params.get("access_token");
    const id_role = params.get("id_role");

    if (access_token && id_role) {
      loginWithOAuth(access_token, parseInt(id_role, 10));
      navigate("/home", { replace: true });
    } else {
      navigate("/sign-in", { replace: true });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location, navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      Вход через OAuth...
    </div>
  );
}
