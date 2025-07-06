import { auth, signOut } from "@/lib/auth";
import axios from "axios";
import camelcaseKeys from "camelcase-keys";
import snakecaseKeys from "snakecase-keys";

export const axiosInstance = axios.create({
  baseURL: process.env.API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

axiosInstance.interceptors.request.use(async (config) => {
  const session = await auth();
  session?.user &&
    config.headers.setAuthorization(`Bearer ${session.user.accessToken}`);

  if (config.data) {
    config.data = toSnakeCase(config.data);
  }

  return config;
});

axiosInstance.interceptors.response.use(
  (response) => {
    if (response.data) {
      response.data = camelcaseKeys(response.data, { deep: true });
    }

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

const isPlainObject = (value: unknown) => {
  return value !== null && typeof value === "object" && !Array.isArray(value);
};

const toSnakeCase = (data: Record<string, unknown>) => {
  if (data instanceof URLSearchParams) {
    const obj: Record<string, string> = {};
    for (const [key, value] of data.entries()) {
      obj[key] = value;
    }
    const snakeObj = snakecaseKeys(obj);
    return new URLSearchParams(snakeObj);
  }

  if (isPlainObject(data)) {
    return snakecaseKeys(data, { deep: true });
  }

  return data;
};
