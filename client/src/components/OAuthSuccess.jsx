import { FcGoogle } from "react-icons/fc";
import { FaYandex } from "react-icons/fa";
import { useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

export default function OAuthSuccess({ baseUrl = "http://localhost:8000" }) {
  const { loginWithOAuth } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get("access_token");
    const id_role = params.get("id_role");
    const email = params.get("email");

    if (token && id_role) {
      localStorage.setItem("access_token", token);
      localStorage.setItem("id_role", id_role);

      loginWithOAuth(token, parseInt(id_role, 10), email || "oauth_user");

      if (parseInt(id_role, 10) === 1) {
        navigate("/admin", { replace: true });
      } else {
        navigate("/home", { replace: true });
      }
    } else {
      navigate("/sign-in", { replace: true });
    }
  }, [loginWithOAuth, navigate]);

  return (
    <div className="flex flex-col items-center gap-4 mt-4">
      <h2 className="text-xl font-semibold mb-2">Войти через:</h2>
      <div className="flex justify-center gap-4">
        <a
          href={`${baseUrl}/oauth/login/google`}
          className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-lg shadow hover:bg-gray-100 transition"
        >
          <FcGoogle className="w-5 h-5" />
          Google
        </a>
        <a
          href={`${baseUrl}/oauth/login/yandex`}
          className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-lg shadow hover:bg-gray-100 transition"
        >
          <FaYandex className="w-5 h-5 text-[#FF0000]" />
          Yandex
        </a>
      </div>
    </div>
  );
}
