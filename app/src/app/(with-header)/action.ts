"use server";

import { parseWithZod } from "@conform-to/zod";
import { redirect } from "next/navigation";
import { paths } from "@/config/paths";
import { serializeArticlesParams } from "@/lib/nuqs/params";
import { searchArticleSchema } from "@/lib/zod/schema";

export async function searchArticle(_prevState: unknown, formData: FormData) {
  const submission = parseWithZod(formData, {
    schema: searchArticleSchema,
  });

  if (submission.status !== "success") {
    return submission.reply();
  }

  redirect(
    serializeArticlesParams(paths.home.getHref(), {
      q: encodeURIComponent(submission.value.q),
    }),
  );
}
