export default function OAuthSuccess({ baseUrl = "http://localhost:8000" }) {
  return (
    <div className="flex flex-col items-center gap-4 mt-4">
      <h2 className="text-xl font-semibold mb-2">Войти через:</h2>
      <div className="flex justify-center gap-4">
        <a
          href={`${baseUrl}/oauth/login/google`}
          className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-lg shadow hover:bg-gray-100 transition"
        >
          Google
        </a>
        <a
          href={`${baseUrl}/oauth/login/yandex`}
          className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-lg shadow hover:bg-gray-100 transition"
        >
          Yandex
        </a>
      </div>
    </div>
  );
}
