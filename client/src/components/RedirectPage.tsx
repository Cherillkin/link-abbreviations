import { useParams } from "react-router-dom";
import { useEffect } from "react";

const RedirectPage = () => {
  const { code } = useParams();

  useEffect(() => {
    const checkLink = async () => {
      try {
        let res = await fetch(`http://localhost:8000/short-links/r/${code}`);
        let data = await res.json();

        if (data.status === "protected") {
          const pwd = prompt("Ссылка защищена. Введите пароль:");
          if (pwd === null) return;

          const verify = await fetch(
            `http://localhost:8000/short-links/verify-password?code=${encodeURIComponent(
              code!
            )}&password=${encodeURIComponent(pwd)}`,
            { method: "POST" }
          );
          const result = await verify.json();

          if (result.status === "ok" || result.status === "not_protected") {
            window.location.href = result.redirect_url;
          } else {
            alert("Неверный пароль");
          }
        } else if (data.redirect_url) {
          window.location.href = data.redirect_url;
        }
      } catch (err) {
        alert("Ошибка: " + err);
      }
    };

    checkLink();
  }, [code]);

  return <p>Проверка ссылки...</p>;
};

export default RedirectPage;
