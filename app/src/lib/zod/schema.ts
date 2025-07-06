import { z } from "zod";
import { message } from "@/lib/zod/message";

const username = z
  .string({ message: message.required("ユーザー名") })
  .min(2, { message: message.min("ユーザー名", 2) })
  .max(8, { message: message.max("ユーザー名", 8) });

const password = z
  .string({ message: message.required("パスワード") })
  .max(100, {
    message: message.max("パスワード", 100),
  });

const articleTitle = z
  .string({ message: message.required("タイトル") })
  .max(200, { message: message.max("タイトル", 200) });

const articleText = z.string().max(20000).optional();

export const loginSchema = z.object({
  username: username,
  password: password,
});

export const signUpSchema = z.object({
  username: username,
  password: password,
});

export const getArticlesQueryParamsSchema = z.object({
  page: z.preprocess((v) => Number(v), z.number()).optional(),
});

export const postArticleSchema = z.object({
  title: articleTitle,
  text: articleText,
});
