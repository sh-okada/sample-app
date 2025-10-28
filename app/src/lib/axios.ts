import axios, { type AxiosError } from "axios";
import applyCaseMiddleware from "axios-case-converter";
import { refreshToken } from "@/api/auth";
import { logout } from "@/app/(with-header)/action";
import {
  getAccessToken,
  getRefreshToken,
  setAccessToken,
  setRefreshToken,
} from "@/utils/cookie";

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
  console.log("access token:", accessToken);
  accessToken && config.headers.setAuthorization(`Bearer ${accessToken}`);

  return config;
});

axiosInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    if (isAccessTokenExpiredError(error)) {
      console.log("refreshing access token...");
      const data =
        // biome-ignore lint/style/noNonNullAssertion: allowed undifined value
        (await refreshToken({ refreshToken: (await getRefreshToken())! })).data;
      setAccessToken(data.accessToken);
      setRefreshToken(data.refreshToken);
      return await axiosInstance.request(error.config || {});
    }

    if (isUnAuthorizedError(error)) {
      await logout();
    }
    return Promise.reject(error);
  },
);

type MessageResponse = {
  detail: string;
};

export const isBadRequestError = (
  error: unknown,
): error is AxiosError<MessageResponse> => {
  return axios.isAxiosError(error) && error.response?.status === 400;
};

export const isUnAuthorizedError = (
  error: unknown,
): error is AxiosError<MessageResponse> => {
  return axios.isAxiosError(error) && error.response?.status === 401;
};

export const isAccessTokenExpiredError = (
  error: unknown,
): error is AxiosError<MessageResponse> => {
  return (
    isUnAuthorizedError(error) &&
    error.response?.data.detail === "Token has expired."
  );
};

export const isRefreshTokenExpiredError = (
  error: unknown,
): error is AxiosError<MessageResponse> => {
  return (
    isUnAuthorizedError(error) &&
    error.response?.data.detail === "Refresh token has expired."
  );
};

export const isNotFoundError = (
  error: unknown,
): error is AxiosError<MessageResponse> => {
  return axios.isAxiosError(error) && error.response?.status === 404;
};

export const isConflictError = (
  error: unknown,
): error is AxiosError<MessageResponse> => {
  return axios.isAxiosError(error) && error.response?.status === 409;
};
