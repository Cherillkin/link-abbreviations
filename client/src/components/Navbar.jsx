import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import axios from "axios";

export default function Navbar() {
  const { logout } = useContext(AuthContext);

  const handleLogout = async () => {
    try {
      await axios.post("/auth/logout", {}, { withCredentials: true });

      logout();
    } catch (err) {
      console.error("Ошибка при выходе:", err.response?.data || err.message);
    }
  };

  return (
    <nav className="bg-gray-800 text-white flex justify-between items-center p-4">
      <div className="text-xl font-bold">ShortLink</div>
      <button
        onClick={handleLogout}
        className="bg-red-600 px-4 py-2 rounded hover:bg-red-700 transition"
      >
        Выйти
      </button>
    </nav>
  );
}
