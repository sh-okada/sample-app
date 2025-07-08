import axios from "axios";
import applyCaseMiddleware from "axios-case-converter";
import { auth, signOut } from "@/lib/auth";

export const axiosInstance = applyCaseMiddleware(
  axios.create({
    baseURL: process.env.API_URL,
    headers: {
      "Content-Type": "application/json",
    },
  }),
);

axiosInstance.interceptors.request.use(async (config) => {
  const session = await auth();
  session?.user &&
    config.headers.setAuthorization(`Bearer ${session.user.accessToken}`);

  return config;
});

axiosInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    if (isUnAuthorizedError(error)) {
      await signOut();
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

export const isConflictError = (error: unknown) => {
  return axios.isAxiosError(error) && error.response?.status === 409;
};
