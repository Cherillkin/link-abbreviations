import { useState, useEffect } from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

import { getShortLinks, getTopLinkStats } from "../api/shortLinks";
import { createAdmin } from "../api/auth";
import { createBackup } from "../api/backup";

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
  const dateFrom = useState("");
  const dateTo = useState("");
  const linksPerPage = 5;

  useEffect(() => {
    const fetchData = async () => {
      try {
        const linksRes = await getShortLinks();
        setShortLinks(linksRes.data);

        const statsRes = await getTopLinkStats();
        setLinkStats(statsRes.data);
      } catch (err) {
        console.error("Ошибка при получении данных:", err);
      }
    };
    fetchData();
  }, []);

  const handleCreateAdmin = async (e) => {
    e.preventDefault();
    try {
      await createAdmin(email, password);
      setMessage("Администратор успешно создан!");
      setEmail("");
      setPassword("");
    } catch (err) {
      console.error(err);
      setMessage("Ошибка при создании администратора");
    }
  };

  const getLinkClicks = (shortCode) => {
    const stat = linkStats.find((s) => s.short_code === shortCode);
    return stat ? stat.clicks : 0;
  };

  const filteredLinks = shortLinks.filter((link) => {
    const createdAt = new Date(link.created_at);
    const from = dateFrom ? new Date(dateFrom) : null;
    const to = dateTo ? new Date(dateTo) : null;

    if (from && createdAt < from) return false;
    if (to && createdAt > to) return false;
    return true;
  });

  const indexOfLastLink = currentPage * linksPerPage;
  const indexOfFirstLink = indexOfLastLink - linksPerPage;
  const currentLinks = filteredLinks.slice(indexOfFirstLink, indexOfLastLink);
  const totalPages = Math.ceil(filteredLinks.length / linksPerPage);

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

  const exportCSV = () => {
    const headers = ["Код", "Оригинальная ссылка", "Переходы"];
    const rows = filteredLinks.map((link) => [
      link.short_code,
      link.original_url,
      getLinkClicks(link.short_code),
    ]);

    let csvContent =
      "data:text/csv;charset=utf-8," +
      [headers, ...rows].map((e) => e.join(",")).join("\n");

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "short_links.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const exportJSON = () => {
    const data = filteredLinks.map((link) => ({
      code: link.short_code,
      url: link.original_url,
      clicks: getLinkClicks(link.short_code),
    }));

    const jsonStr = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonStr], { type: "application/json" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "short_links.json";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
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

        <div className="flex justify-center mt-4 gap-2">
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

        <div className="mt-4 flex justify-center gap-2">
          <button
            onClick={exportCSV}
            className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
          >
            Экспорт CSV
          </button>
          <button
            onClick={exportJSON}
            className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
          >
            Экспорт JSON
          </button>
        </div>
      </div>

      <div className="bg-white p-4 rounded shadow mb-6">
        <h2 className="text-xl font-bold mb-4">Статистика переходов</h2>
        <Bar data={chartData} />
      </div>

      <button
        onClick={createBackup}
        className="relative top-2 bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
      >
        Скачать бэкап
      </button>
    </div>
  );
}
