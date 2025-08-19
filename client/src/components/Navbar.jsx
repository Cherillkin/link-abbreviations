import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { Link } from "react-router-dom";
import { logout as logoutApi } from "../api/auth";

export default function Navbar() {
  const { logout, user } = useContext(AuthContext);

  const handleLogout = async () => {
    try {
      await logoutApi();
      logout();
    } catch (err) {
      console.error("Ошибка при выходе:", err.response?.data || err.message);
      throw err;
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
