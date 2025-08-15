import { useState, useEffect } from "react";
import axios from "axios";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export default function AdminDashboard() {
  const [shortLinks, setShortLinks] = useState([]);
  const [linkStats, setLinkStats] = useState([]);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const linksPerPage = 5;

  useEffect(() => {
    const fetchShortLinks = async () => {
      try {
        const res = await axios.get("http://localhost:8000/short-links");
        setShortLinks(res.data);
      } catch (err) {
        console.error("Ошибка при получении коротких ссылок:", err);
      }
    };

    const fetchLinkStats = async () => {
      try {
        const res = await axios.get(
          "http://localhost:8000/short-links/stats/top-links"
        );
        setLinkStats(res.data);
      } catch (err) {
        console.error("Ошибка при получении статистики переходов:", err);
      }
    };

    fetchShortLinks();
    fetchLinkStats();
  }, []);

  const handleCreateAdmin = async (e) => {
    e.preventDefault();
    try {
      await axios.post(
        "http://localhost:8000/auth/create",
        { email, password },
        { withCredentials: true }
      );
      setMessage("Администратор успешно создан!");
      setEmail("");
      setPassword("");
    } catch (err) {
      console.error(err);
      setMessage("Ошибка при создании администратора");
    }
  };

  const chartData = {
    labels: linkStats.map((s) => s.short_code),
    datasets: [
      {
        label: "Количество переходов",
        data: linkStats.map((s) => s.clicks),
        backgroundColor: "rgba(59, 130, 246, 0.7)",
      },
    ],
  };

  const indexOfLastLink = currentPage * linksPerPage;
  const indexOfFirstLink = indexOfLastLink - linksPerPage;
  const currentLinks = shortLinks.slice(indexOfFirstLink, indexOfLastLink);
  const totalPages = Math.ceil(shortLinks.length / linksPerPage);

  const getLinkClicks = (shortCode) => {
    const stat = linkStats.find((s) => s.short_code === shortCode);
    return stat ? stat.clicks : 0;
  };

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="flex justify-center text-3xl font-bold mb-6">
        Админ-панель
      </h1>

      <div className="bg-white p-4 rounded shadow mb-6">
        <h2 className="text-xl font-bold mb-4">Создать администратора</h2>
        <form onSubmit={handleCreateAdmin} className="flex gap-4 flex-wrap">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="border px-3 py-2 rounded w-64"
          />
          <input
            type="password"
            placeholder="Пароль"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="border px-3 py-2 rounded w-64"
          />
          <button
            type="submit"
            className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
          >
            Создать
          </button>
        </form>
        {message && <p className="mt-2 text-sm text-blue-700">{message}</p>}
      </div>

      <div className="bg-white p-4 rounded shadow mb-6 overflow-x-auto">
        <h2 className="text-xl font-bold mb-4">Список коротких ссылок</h2>
        <table className="w-full border-collapse border">
          <thead>
            <tr className="bg-gray-100">
              <th className="border px-3 py-2">Код</th>
              <th className="border px-3 py-2">Оригинальная ссылка</th>
              <th className="border px-3 py-2">Переходы</th>
            </tr>
          </thead>
          <tbody>
            {currentLinks.map((link) => (
              <tr key={link.id}>
                <td className="border px-3 py-2">{link.short_code}</td>
                <td className="border px-3 py-2">{link.original_url}</td>
                <td className="border px-3 py-2">
                  {getLinkClicks(link.short_code)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        <div className="flex justify-center mt-4 gap-2 flex-wrap">
          {Array.from({ length: totalPages }, (_, idx) => (
            <button
              key={idx + 1}
              onClick={() => setCurrentPage(idx + 1)}
              className={`px-3 py-1 rounded border ${
                currentPage === idx + 1
                  ? "bg-blue-500 text-white"
                  : "bg-white text-black"
              }`}
            >
              {idx + 1}
            </button>
          ))}
        </div>
      </div>

      <div className="bg-white p-4 rounded shadow">
        <h2 className="text-xl font-bold mb-4">Статистика переходов</h2>
        <Bar data={chartData} />
      </div>
    </div>
  );
}
