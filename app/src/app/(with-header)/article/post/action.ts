"use server";

import { parseWithZod } from "@conform-to/zod";
import { redirect } from "next/navigation";
import { postArticle as postArticleApi } from "@/api/articles";
import { paths } from "@/config/paths";
import { postArticleSchema } from "@/lib/zod/schema";

export async function postArticle(_prevState: unknown, formData: FormData) {
  const submission = parseWithZod(formData, {
    schema: postArticleSchema,
  });

  if (submission.status !== "success") {
    return submission.reply();
  }

  await postArticleApi(submission.value);

  redirect(paths.home.getHref());
}
