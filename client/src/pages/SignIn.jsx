import { useState, useContext, useEffect } from "react";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function SignIn() {
  const { login, isAuthenticated, user } = useContext(AuthContext);
  const [form, setForm] = useState({ email: "", password: "" });
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      await login(form.email, form.password);
      setMessage("Вход успешен!");
    } catch (err) {
      setMessage(
        "Ошибка входа: " + (err.response?.data?.detail || err.message)
      );
    }
  };

  useEffect(() => {
    if (isAuthenticated && user) {
      if (user.id_role === 1) {
        navigate("/admin");
      } else {
        navigate("/");
      }
    }
  }, [isAuthenticated, user, navigate]);

  return (
    <div className="max-w-md w-full mx-auto p-6 bg-white rounded-2xl shadow-md">
      <h2 className="text-2xl font-bold mb-6 text-center">Вход</h2>

      <form onSubmit={handleSubmit} className="flex flex-col">
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
          required
          className="w-full mb-4 p-3 border border-gray-300 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <input
          type="password"
          name="password"
          placeholder="Пароль"
          value={form.password}
          onChange={handleChange}
          required
          className="w-full mb-6 p-3 border border-gray-300 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          className="w-full bg-green-600 text-white py-3 rounded-2xl hover:bg-green-700 transition mb-4"
        >
          Войти
        </button>
      </form>

      {message && (
        <p className="mt-4 text-center text-sm text-red-600">{message}</p>
      )}
    </div>
  );
}
