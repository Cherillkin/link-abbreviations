import { useState, useContext } from "react";
import axios from "axios";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import OAuthSuccess from "../components/OAuthSuccess";

export default function SignUp() {
  const { login } = useContext(AuthContext);
  const [form, setForm] = useState({ email: "", password: "" });
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/auth/sign-in",
        form
      );
      const { access_token, id_role } = response.data;

      login(access_token, id_role);
      localStorage.setItem("access_token", access_token);
      localStorage.setItem("id_role", id_role);

      setMessage("Вход успешен!");
      if (id_role === 1) {
        navigate("/admin");
      } else {
        navigate("/");
      }
    } catch (err) {
      setMessage(
        "Ошибка входа: " + (err.response?.data?.detail || err.message)
      );
    }
  };

  return (
    <div className="max-w-md w-full mx-auto p-6 bg-white rounded-2xl shadow-md">
      <h2 className="text-2xl font-bold mb-6 text-center">Регистрация</h2>

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
          Зарегистрироваться
        </button>
      </form>

      <OAuthSuccess baseUrl="http://127.0.0.1:8000" />

      {message && (
        <p className="mt-4 text-center text-sm text-red-600">{message}</p>
      )}
    </div>
  );
}
