// src/services/api.ts
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000", // backend
  withCredentials: true,           // envia e recebe cookies
});

export default api;
