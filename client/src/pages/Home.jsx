import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { Link } from "react-router-dom";

export default function Home() {
  const { isAuthenticated } = useContext(AuthContext);

  if (!isAuthenticated) {
    return (
      <div className="text-center p-8">
        <h2 className="text-2xl font-semibold mb-4">
          Пожалуйста, войдите или зарегистрируйтесь
        </h2>
        <div className="space-x-4">
          <Link
            to="/sign-in"
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
          >
            Войти
          </Link>
          <Link
            to="/sign-up"
            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition"
          >
            Регистрация
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-4">Добро пожаловать!</h1>
      <p>Вы успешно вошли в систему.</p>
    </div>
  );
}
