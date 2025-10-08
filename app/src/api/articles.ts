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

export type ArticlesResponse = {
  values: ArticleResponse[];
  count: number;
  totalPages: number;
};

export type PostArticleRequest = z.infer<typeof postArticleSchema>;

export const getArticle = async (id: string) =>
  axiosInstance.get<ArticleResponse>(`/articles/${id}`);

export const getArticles = async (page: number, q: string) =>
  axiosInstance.get<ArticlesResponse>("/articles", {
    params: { page: page, q: q, limit: 5 },
  });

export const postArticle = async (data: PostArticleRequest) =>
  axiosInstance.post("/articles", data);
