"use client";

import { getFormProps, getInputProps, useForm } from "@conform-to/react";
import { parseWithZod } from "@conform-to/zod";
import { useActionState } from "react";
import { signup } from "@/app/(without-header)/signup/action";
import { Button } from "@/components/core/button";
import { ErrorText } from "@/components/core/error-text";
import { Field } from "@/components/core/field";
import { Input } from "@/components/core/input";
import { Link } from "@/components/core/link";
import { InternalLink } from "@/components/ui-parts/internal-link";
import { paths } from "@/config/paths";
import { signUpSchema } from "@/lib/zod/schema";

export const SignUpForm = () => {
  const [lastResult, action] = useActionState(signup, null);
  const [form, fields] = useForm({
    lastResult,
    onValidate({ formData }) {
      return parseWithZod(formData, { schema: signUpSchema });
    },
    shouldValidate: "onBlur",
  });

  return (
    <form {...getFormProps(form)} action={action}>
      <ErrorText>{form.errors}</ErrorText>
      <div className="flex flex-col gap-2">
        <Field>
          <Field.Label htmlFor={fields.username.id}>ユーザー名</Field.Label>
          <Input
            {...getInputProps(fields.username, { type: "text" })}
            key={fields.username.key}
          />
          <ErrorText>{fields.username.errors}</ErrorText>
        </Field>
        <Field>
          <Field.Label htmlFor={fields.password.id}>パスワード</Field.Label>
          <Input
            {...getInputProps(fields.password, { type: "password" })}
            key={fields.password.key}
          />
          <ErrorText>{fields.password.errors}</ErrorText>
        </Field>
        <Button type="submit">登録</Button>
        <div className="text-right">
          <Link asChild>
            <InternalLink href={paths.login.getHref()}>
              ログインはこちら
            </InternalLink>
          </Link>
        </div>
      </div>
    </form>
  );
};
