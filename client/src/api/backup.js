import axios from "axios";

export const createBackup = async () => {
  try {
    const response = await axios.post(
      "http://localhost:8000/backup",
      {},
      {
        responseType: "blob",
        withCredentials: true,
      }
    );

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;

    const contentDisposition = response.headers["content-disposition"];
    const filename = contentDisposition
      ? contentDisposition.split("filename=")[1].replace(/"/g, "")
      : "backup.sql";

    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
  } catch (error) {
    console.error("Ошибка при создании бэкапа:", error);
    alert("Не удалось создать бэкап");
  }
};
