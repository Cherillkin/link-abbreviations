import { useState, useEffect } from "react";
import QRCode from "qrcode";
import {
  createShortLink,
  getShortUser,
  deleteShortUser,
} from "../api/shortLinks";

const Home = () => {
  const [originalUrl, setOriginalUrl] = useState("");
  const [customCode, setCustomCode] = useState("");
  const [expiresAt, setExpiresAt] = useState("");
  const [isProtected, setIsProtected] = useState(false);
  const [password, setPassword] = useState("");
  const [shortLink, setShortLink] = useState(null);
  const [qrImage, setQrImage] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const [drawerOpen, setDrawerOpen] = useState(false);
  const [userLinks, setUserLinks] = useState([]);
  const [linksLoading, setLinksLoading] = useState(false);

  // Создание короткой ссылки
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setShortLink(null);
    setQrImage(null);
    setLoading(true);

    try {
      const payload = { original_url: originalUrl, is_protected: isProtected };
      if (customCode) payload.custom_code = customCode;
      if (expiresAt) payload.expires_at = expiresAt;
      if (isProtected && password) payload.password = password;

      const response = await createShortLink(payload);
      const short_code = response.data.short_code;
      if (!short_code) throw new Error("Нет short_code в ответе сервера");

      const frontendLink = `http://localhost:5173/short-links/r/${short_code}`;
      setShortLink(frontendLink);

      const qrDataUrl = await QRCode.toDataURL(frontendLink);
      setQrImage(qrDataUrl);

      if (drawerOpen) loadUserLinks();
    } catch (err) {
      setError(
        err.response?.data?.detail || err.message || "Ошибка создания ссылки"
      );
    } finally {
      setLoading(false);
    }
  };

  const loadUserLinks = async () => {
    setLinksLoading(true);
    try {
      const response = await getShortUser();
      setUserLinks(response.data);
    } catch (err) {
      setError("Ошибка загрузки ссылок: ", err);
    } finally {
      setLinksLoading(false);
    }
  };

  const handleDelete = async (short_code) => {
    try {
      await deleteShortUser(short_code);
      setUserLinks(userLinks.filter((link) => link.short_code !== short_code));
    } catch (err) {
      setError("Ошибка удаления ссылки: ", err);
    }
  };

  useEffect(() => {
    if (drawerOpen) loadUserLinks();
  }, [drawerOpen]);

  return (
    <div className="relative flex bg-gray-100">
      {/* Основной контент */}
      <div className="flex-1 max-w-lg mx-auto p-6 mt-10 bg-white shadow-lg rounded-lg">
        <h1 className="text-2xl font-bold mb-6 text-center">
          Создать короткую ссылку
        </h1>

        <button
          className="mb-4 bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded-md"
          onClick={() => setDrawerOpen(!drawerOpen)}
        >
          {drawerOpen ? "Закрыть мои ссылки" : "Мои ссылки"}
        </button>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="flex justify-center m-2 text-gray-700 text-base">
              Оригинальная ссылка:
            </label>
            <input
              type="url"
              value={originalUrl}
              onChange={(e) => setOriginalUrl(e.target.value)}
              required
              className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
          </div>

          <div>
            <label className="flex justify-center m-2 text-gray-700 text-base">
              Кастомный код (необязательно):
            </label>
            <input
              type="text"
              value={customCode}
              onChange={(e) => setCustomCode(e.target.value)}
              className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
          </div>

          <div className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={isProtected}
              onChange={(e) => setIsProtected(e.target.checked)}
              className="w-4 h-4"
            />
            <label className="text-gray-700">Ссылка защищена паролем</label>
          </div>

          {isProtected && (
            <div>
              <label className="block text-gray-700">Пароль:</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
            </div>
          )}

          <div>
            <label className="flex justify-center m-2 text-gray-700 text-base">
              Дата истечения (необязательно):
            </label>
            <input
              type="datetime-local"
              value={expiresAt}
              onChange={(e) => setExpiresAt(e.target.value)}
              className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-md transition-colors disabled:opacity-50"
          >
            {loading ? "Создание..." : "Создать короткую ссылку"}
          </button>
        </form>

        {shortLink && (
          <div className="mt-4 p-4 bg-green-100 border border-green-300 rounded-md">
            <strong>Ваша короткая ссылка:</strong>{" "}
            <a
              href={shortLink}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 underline"
            >
              {shortLink}
            </a>
          </div>
        )}

        {qrImage && (
          <div className="mt-4 p-4 bg-gray-100 border border-gray-300 rounded-md flex justify-center">
            <img src={qrImage} alt="QR Code" className="w-48 h-48" />
          </div>
        )}

        {error && (
          <div className="mt-4 p-4 bg-red-100 border border-red-300 rounded-md text-red-700">
            <strong>Ошибка:</strong> {error}
          </div>
        )}
      </div>

      {/* Drawer */}
      <div
        className={`fixed top-0 right-0 h-full w-110 bg-white shadow-lg transform transition-transform duration-300 ${
          drawerOpen ? "translate-x-0" : "translate-x-full"
        } z-50 p-6 overflow-y-auto`}
      >
        <h2 className="text-xl font-bold mb-4">Мои ссылки</h2>
        {linksLoading ? (
          <p>Загрузка ссылок...</p>
        ) : userLinks.length === 0 ? (
          <p>Вы еще не создали ни одной ссылки.</p>
        ) : (
          <ul className="space-y-2">
            {userLinks.map((link) => (
              <li
                key={link.short_code}
                className="flex justify-between items-center p-2 bg-gray-50 border rounded-md"
              >
                <div>
                  <a
                    href={`http://localhost:5173/short-links/r/${link.short_code}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 underline"
                  >
                    {link.short_code}
                  </a>
                  <p className="text-gray-600 text-sm truncate w-64">
                    {link.original_url}
                  </p>
                </div>
                <button
                  onClick={() => handleDelete(link.short_code)}
                  className="bg-red-500 hover:bg-red-600 text-white font-bold py-1 px-3 rounded-md"
                >
                  Удалить
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default Home;
