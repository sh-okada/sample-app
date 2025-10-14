import type { z } from "zod";
import { axiosInstance } from "@/lib/axios";
import type { likeArticleSchema } from "@/lib/zod/schema";

export type LikeArticleResponse = {
  id: string;
  title: string;
  text: string;
  publishedAt: Date;
  user: {
    id: string;
    name: string;
  };
};

export type LikeArticleRequest = z.infer<typeof likeArticleSchema>;

export const getLikedArticle = async (id: string) =>
  axiosInstance.get<LikeArticleResponse>(`/users/me/liked-articles/${id}`);

export const likeArticle = async (data: LikeArticleRequest) =>
  axiosInstance.post("/users/me/liked-articles", data);

export const unlikeArticle = async (id: string) =>
  axiosInstance.delete(`/users/me/liked-articles/${id}`);
