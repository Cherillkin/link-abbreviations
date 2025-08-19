import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import { signUp, signIn } from "../api/auth";
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
    setMessage("");

    try {
      await signUp(form.email, form.password);
      const data = await signIn(form.email, form.password);
      const { access_token, id_role } = data;

      login(access_token, id_role);
      localStorage.setItem("access_token", access_token);
      localStorage.setItem("id_role", id_role);

      navigate(id_role === 1 ? "/admin" : "/home");
    } catch (err) {
      setMessage(
        "Ошибка регистрации: " + (err.response?.data?.detail || err.message)
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

      <OAuthSuccess />

      <p className="mt-4 text-center text-sm">
        Уже есть аккаунт?{" "}
        <span
          className="text-blue-500 hover:underline cursor-pointer"
          onClick={() => navigate("/sign-in")}
        >
          Войти
        </span>
      </p>

      {message && (
        <p className="mt-4 text-center text-sm text-red-600">{message}</p>
      )}
    </div>
  );
}
