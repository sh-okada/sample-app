import axios from "axios";
import applyCaseMiddleware from "axios-case-converter";
import { logout } from "@/app/(with-header)/action";
import { getAccessToken } from "@/utils/cookie";

export const axiosInstance = applyCaseMiddleware(
  axios.create({
    baseURL: process.env.API_URL,
    headers: {
      "Content-Type": "application/json",
    },
    adapter: "fetch",
  }),
);

axiosInstance.interceptors.request.use(async (config) => {
  const accessToken = await getAccessToken();
  accessToken && config.headers.setAuthorization(`Bearer ${accessToken}`);

  return config;
});

axiosInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    if (isUnAuthorizedError(error)) {
      await logout();
    }
    return Promise.reject(error);
  },
);

export const isBadRequestError = (error: unknown) => {
  return axios.isAxiosError(error) && error.response?.status === 400;
};

export const isUnAuthorizedError = (error: unknown) => {
  return axios.isAxiosError(error) && error.response?.status === 401;
};

export const isNotFoundError = (error: unknown) => {
  return axios.isAxiosError(error) && error.response?.status === 404;
};

export const isConflictError = (error: unknown) => {
  return axios.isAxiosError(error) && error.response?.status === 409;
};
