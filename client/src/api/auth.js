import axios from "axios";

const API_URL = "http://localhost:8000";

export const createAdmin = async (email, password) => {
  await axios.post(
    `${API_URL}/auth/create`,
    { email, password },
    { withCredentials: true }
  );
};

export const signUp = async (email, password) => {
  await axios.post(
    `${API_URL}/auth/sign-up`,
    { email, password },
    { withCredentials: true }
  );
};

export const signIn = async (email, password) => {
  const response = await axios.post(
    `${API_URL}/auth/sign-in`,
    { email, password },
    { withCredentials: true }
  );
  return response.data;
};

export const logout = async () => {
  await axios.post(`${API_URL}/auth/logout`, {}, { withCredentials: true });
};
