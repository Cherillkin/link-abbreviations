import { useState } from "react";
import QRCode from "qrcode";
import { createShortLink } from "../api/shortLinks";

const Home = () => {
  const [originalUrl, setOriginalUrl] = useState("");
  const [customCode, setCustomCode] = useState("");
  const [expiresAt, setExpiresAt] = useState("");
  const [isProtected, setIsProtected] = useState(false);
  const [password, setPassword] = useState("");
  const [shortLink, setShortLink] = useState(null);
  const [qrImage, setQrImage] = useState(null);
  const [error, setError] = useState("");
  const [loadingQr, setLoadingQr] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setShortLink(null);
    setQrImage(null);

    try {
      const payload = { original_url: originalUrl, is_protected: isProtected };
      if (customCode) payload.custom_code = customCode;
      if (expiresAt) payload.expires_at = expiresAt;
      if (isProtected && password) payload.password = password;

      const response = await createShortLink(payload);

      const short_code = response.data.short_code;
      if (!short_code) throw new Error("Нет short_code в ответе сервера");

      setShortLink(`${"http://localhost:8000"}/short-links/r/${short_code}`);
    } catch (err) {
      setError(
        err.response?.data?.detail || err.message || "Ошибка создания ссылки"
      );
    }
  };

  const handleGenerateQr = async () => {
    if (!shortLink) return;
    setError("");
    setLoadingQr(true);
    setQrImage(null);

    try {
      const qrDataUrl = await QRCode.toDataURL(shortLink);
      setQrImage(qrDataUrl);
    } catch {
      setError("Ошибка генерации QR-кода");
    } finally {
      setLoadingQr(false);
    }
  };

  return (
    <div className="max-w-lg mx-auto p-6 bg-white shadow-lg rounded-lg mt-10">
      <h1 className="text-2xl font-bold mb-6 text-center">
        Создать короткую ссылку
      </h1>
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
          className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-md transition-colors"
        >
          Создать короткую ссылку
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
          <button
            onClick={handleGenerateQr}
            className="mt-2 w-full bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded-md transition-colors"
          >
            Сгенерировать QR-код
          </button>
        </div>
      )}

      {loadingQr && (
        <div className="mt-4 text-gray-700">Генерация QR-кода...</div>
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
  );
};

export default Home;
