import { useState, useContext } from "react";
import axios from "axios";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function SignIn() {
  const { login } = useContext(AuthContext);
  const [form, setForm] = useState({ email: "", password: "" });
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("/auth/sign-in", form, {
        withCredentials: true,
      });

      login(response.data.access_token);

      setMessage("Вход успешен!");
      navigate("/");
    } catch (err) {
      setMessage(
        "Ошибка входа: " + (err.response?.data?.detail || err.message)
      );
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="max-w-md w-full mx-auto p-6 bg-white rounded-2xl shadow-md"
    >
      <h2 className="text-2xl font-bold mb-6 text-center">Вход</h2>

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
        className="w-full bg-green-600 text-white py-3 rounded-2xl hover:bg-green-700 transition"
      >
        Войти
      </button>

      {message && (
        <p className="mt-4 text-center text-sm text-red-600">{message}</p>
      )}
    </form>
  );
}
