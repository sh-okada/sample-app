import type { z } from "zod";
import { axiosInstance } from "@/lib/axios";
import type { loginSchema, signUpSchema } from "@/lib/zod/schema";

export type LoginResponse = {
  userId: string;
  username: string;
  accessToken: string;
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
