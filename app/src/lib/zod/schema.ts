import { z } from "zod";
import { message } from "@/lib/zod/message";

export const loginSchema = z.object({
  username: z
    .string({ message: message.required("ユーザー名") })
    .min(2, { message: message.min("ユーザー名", 2) })
    .max(8, { message: message.max("ユーザー名", 8) }),
  password: z.string({ message: message.required("パスワード") }).max(100, {
    message: message.max("パスワード", 100),
  }),
});

export const signUpSchema = z.object({
  username: z
    .string({ message: message.required("ユーザー名") })
    .min(2, { message: message.min("ユーザー名", 2) })
    .max(8, { message: message.max("ユーザー名", 8) })
    .regex(/^[a-zA-Z0-9._-]+$/, {
      message: message.regex(
        "ユーザー名は半角英数字と記号（._-）で入力してください",
      ),
    }),
  password: z
    .string({ message: message.required("パスワード") })
    .max(100, {
      message: message.max("パスワード", 100),
    })
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/, {
      message: message.regex(
        "パスワードには半角英（大文字・小文字）数字が含まれている必要があります",
      ),
    }),
});

export const postArticleSchema = z.object({
  title: z
    .string({ message: message.required("タイトル") })
    .max(200, { message: message.max("タイトル", 200) }),
  text: z.string().max(20000).default(""),
});

export const searchArticleSchema = z.object({
  q: z
    .string({ message: message.required("検索ワード") })
    .max(100, { message: message.max("検索ワード", 100) }),
});
