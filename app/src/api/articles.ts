import type { z } from "zod";
import { axiosInstance } from "@/lib/axios";
import type { postArticleSchema } from "@/lib/zod/schema";

export type ArticleResponse = {
  id: string;
  title: string;
  text: string;
  user: {
    id: string;
    name: string;
  };
};

export type ArticleCount = {
  count: number;
};

export type PostArticleRequest = z.infer<typeof postArticleSchema>;

export const getArticle = async (id: string) =>
  axiosInstance.get<ArticleResponse>(`/articles/${id}`);

export const getArticles = async (page: number) =>
  axiosInstance.get<ArticleResponse[]>(`/articles?page=${page}`);

export const getArticleCount = async () =>
  axiosInstance.get<ArticleCount>("/articles/count");

export const postArticle = async (data: PostArticleRequest) =>
  axiosInstance.post("/articles", data);
