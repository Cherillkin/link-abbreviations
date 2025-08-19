import axios from "axios";

const API_URL = "http://localhost:8000";

export const getShortLinks = () => axios.get(`${API_URL}/short-links`);

export const getTopLinkStats = () =>
  axios.get(`${API_URL}/short-links/stats/top-links`);

export const createShortLink = (payload) =>
  axios.post(`${API_URL}/short-links/`, payload, { withCredentials: true });
