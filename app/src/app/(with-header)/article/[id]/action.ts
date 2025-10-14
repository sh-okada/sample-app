"use server";

import { parseWithZod } from "@conform-to/zod";
import { revalidatePath } from "next/cache";
import { likeArticle, unlikeArticle } from "@/api/users";
import { likeArticleSchema } from "@/lib/zod/schema";

export async function like(_prevState: unknown, formData: FormData) {
  const submission = parseWithZod(formData, {
    schema: likeArticleSchema,
  });

  if (submission.status !== "success") {
    return submission.reply();
  }

  await likeArticle(submission.value);

  return revalidatePath(`/article/${submission.value.articleId}`);
}

export async function unlike(_prevState: unknown, formData: FormData) {
  const submission = parseWithZod(formData, {
    schema: likeArticleSchema,
  });

  if (submission.status !== "success") {
    return submission.reply();
  }

  await unlikeArticle(submission.value.articleId);

  return revalidatePath(`/article/${submission.value.articleId}`);
}
