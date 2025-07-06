"use server";

import { parseWithZod } from "@conform-to/zod";
import { AuthError } from "next-auth";
import { signIn } from "@/lib/auth";
import { isBadRequestError } from "@/lib/axios";
import { loginSchema } from "@/lib/zod/schema";

export async function login(_prevState: unknown, formData: FormData) {
  const submission = parseWithZod(formData, {
    schema: loginSchema,
  });

  if (submission.status !== "success") {
    return submission.reply();
  }

  try {
    await signIn("credentials", {
      ...Object.fromEntries(formData),
      redirect: true,
    });
  } catch (error) {
    if (error instanceof AuthError && isBadRequestError(error.cause?.err)) {
      return submission.reply({
        formErrors: ["ユーザ名またはパスワードが間違っています。"],
      });
    }
    throw error;
  }
}
