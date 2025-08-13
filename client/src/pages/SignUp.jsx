import { useState } from "react";
import axios from "axios";

export default function SignUp() {
  const [form, setForm] = useState({
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Проверка совпадения паролей
    if (form.password !== form.confirmPassword) {
      setMessage("Пароли не совпадают!");
      return;
    }

    try {
      const response = await axios.post(
        "/auth/sign-up",
        {
          email: form.email,
          password: form.password,
        },
        { withCredentials: true }
      );

      setMessage("Регистрация успешна! Токен: " + response.data.access_token);
    } catch (err) {
      setMessage(
        "Ошибка регистрации: " + (err.response?.data?.detail || err.message)
      );
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="max-w-md mx-auto p-6 bg-white rounded-2xl shadow-md"
    >
      <h2 className="text-2xl font-bold mb-6 text-center">Регистрация</h2>
      <input
        type="text"
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
        className="w-full mb-4 p-3 border border-gray-300 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <input
        type="password"
        name="confirmPassword"
        placeholder="Повторный Пароль"
        value={form.confirmPassword}
        onChange={handleChange}
        required
        className="w-full mb-6 p-3 border border-gray-300 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        type="submit"
        className="w-full bg-blue-600 text-white py-3 rounded-2xl hover:bg-blue-700 transition"
      >
        Зарегистрироваться
      </button>
      {message && (
        <p className="mt-4 text-center text-sm text-red-600">{message}</p>
      )}
    </form>
  );
}
