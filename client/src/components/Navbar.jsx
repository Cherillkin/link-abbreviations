import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import axios from "axios";
import { Link } from "react-router-dom";

export default function Navbar() {
  const { logout, user } = useContext(AuthContext);

  const handleLogout = async () => {
    try {
      await axios.post(
        "http://127.0.0.1:8000/auth/logout",
        {},
        { withCredentials: true }
      );
      logout();
    } catch (err) {
      console.error("Ошибка при выходе:", err.response?.data || err.message);
    }
  };

  return (
    <nav className="bg-gray-800 text-white flex justify-between items-center p-4">
      <div className="flex items-center space-x-4">
        <Link to="/home" className="text-xl font-bold">
          ShortLink
        </Link>
        {user?.id_role === 1 && (
          <Link
            to="/admin"
            className="bg-blue-600 px-3 py-1 rounded hover:bg-blue-700 transition"
          >
            Админ-панель
          </Link>
        )}
      </div>
      <button
        onClick={handleLogout}
        className="bg-red-600 px-4 py-2 rounded hover:bg-red-700 transition"
      >
        Выйти
      </button>
    </nav>
  );
}
