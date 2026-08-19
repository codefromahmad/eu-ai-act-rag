import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "/api",
  timeout: 180000,
});

export const createReport = async (file) => {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post("/documents/report", formData);

  return response.data;
};

export const extractDocument = async (file) => {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post("/documents/extract", formData);

  return response.data;
};

export const analyzeDocument = async (file) => {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post("/documents/analyze", formData);

  return response.data;
};

export const getAnalyses = async () => {
  const response = await api.get("/analyses");

  return response.data;
};

export const getAnalysis = async (analysisId) => {
  const response = await api.get(`/analyses/${analysisId}`);

  return response.data;
};

export const getHealth = async () => {
  const response = await api.get("/health");

  return response.data;
};

export const getReadiness = async () => {
  const response = await api.get("/ready");

  return response.data;
};

export default api;
