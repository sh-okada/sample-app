"use server";

import { parseWithZod } from "@conform-to/zod";
import { redirect } from "next/navigation";
import { signup as signupApi } from "@/api/auth";
import { paths } from "@/config/paths";
import { isBadRequestError } from "@/lib/axios";
import { signUpSchema } from "@/lib/zod/schema";

export async function signup(_prevState: unknown, formData: FormData) {
  const submission = parseWithZod(formData, {
    schema: signUpSchema,
  });

  if (submission.status !== "success") {
    return submission.reply();
  }

  try {
    await signupApi(submission.value);
    return redirect(paths.login.getHref());
  } catch (error) {
    if (isBadRequestError(error)) {
      return submission.reply({
        formErrors: ["ユーザー名は既に使用されています。"],
      });
    }
    throw error;
  }
}
