import type { z } from "zod";
import { axiosInstance } from "@/lib/axios";
import type { loginSchema, signUpSchema } from "@/lib/zod/schema";

export type LoginResponse = {
  id: string;
  username: string;
  accessToken: string;
  refreshToken: string;
};

export type LoginRequest = z.infer<typeof loginSchema>;

export const login = async (data: LoginRequest) =>
  axiosInstance.post<LoginResponse>("/auth/login", new URLSearchParams(data), {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

export type SignUpRequest = z.infer<typeof signUpSchema>;

export const signup = async (data: SignUpRequest) =>
  axiosInstance.post("/auth/signup", data);

export type TokenResponse = {
  accessToken: string;
  refreshToken: string;
};

export type RefreshTokenRequest = {
  refreshToken: string;
};

export const refreshToken = async (data: RefreshTokenRequest) =>
  axiosInstance.post<TokenResponse>("/auth/tokens/refresh", data);
