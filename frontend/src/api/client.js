import axios from "axios";

const baseURL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") || "http://127.0.0.1:8000/api";

const apiClient = axios.create({
  baseURL: baseURL.endsWith("/api") ? baseURL : `${baseURL}/api`,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

export const getTickers = async () => {
  const { data } = await apiClient.get("/tickers");
  return data;
};

export const trainModels = async ({ ticker, start_date }) => {
  const { data } = await apiClient.post("/train", { ticker, start_date });
  return data;
};

export const predictStock = async ({ ticker }) => {
  const { data } = await apiClient.post("/predict", { ticker });
  return data;
};

export const getHistory = async (ticker) => {
  const { data } = await apiClient.get(`/history/${ticker}`);
  return data;
};

export default apiClient;
