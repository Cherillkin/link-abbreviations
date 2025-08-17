import { useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import { FcGoogle } from "react-icons/fc";
import { FaYandex } from "react-icons/fa";
import Cookies from "js-cookie";

export default function OAuthSuccess({ baseUrl = "http://localhost:8000" }) {
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    const token = Cookies.get("access_token");
    const id_role = parseInt(Cookies.get("id_role"), 10);

    if (token && !isNaN(id_role)) {
      login(token, id_role);
      navigate("/", { replace: true });
    } else {
      navigate("/sign-in", { replace: true });
    }
  }, [login, navigate]);

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
