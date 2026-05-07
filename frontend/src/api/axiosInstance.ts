import axios, { type AxiosError } from 'axios'

const BASE_URL = (import.meta as any).env?.VITE_API_BASE_URL ?? 'http://localhost:8000/api'

export const axiosInstance = axios.create({
  baseURL: BASE_URL,
  withCredentials: true,
  headers: { 'Content-Type': 'application/json' },
  timeout: 30_000,
})

axiosInstance.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => Promise.reject(error),
)

export default axiosInstance
