"use client";

import { getFormProps, getInputProps, useForm } from "@conform-to/react";
import { parseWithZod } from "@conform-to/zod";
import { useActionState } from "react";
import { login } from "@/app/(without-header)/login/action";
import { Button } from "@/components/core/button";
import { ErrorText } from "@/components/core/error-text";
import { Field } from "@/components/core/field";
import { Input } from "@/components/core/input";
import { Link } from "@/components/core/link";
import { InternalLink } from "@/components/ui-parts/internal-link";
import { paths } from "@/config/paths";
import { loginSchema } from "@/lib/zod/schema";

export const LoginForm = () => {
  const [lastResult, action] = useActionState(login, null);
  const [form, fields] = useForm({
    lastResult,
    onValidate({ formData }) {
      return parseWithZod(formData, { schema: loginSchema });
    },
    shouldValidate: "onBlur",
  });

  return (
    <form {...getFormProps(form)} action={action}>
      <ErrorText data-testid="error-text">{form.errors}</ErrorText>
      <div className="flex flex-col gap-2">
        <Field>
          <Field.Label htmlFor={fields.username.id}>ユーザー名</Field.Label>
          <Input
            data-testid="username-input"
            {...getInputProps(fields.username, { type: "text" })}
            key={fields.username.key}
          />
          <ErrorText>{fields.username.errors}</ErrorText>
        </Field>
        <Field>
          <Field.Label htmlFor={fields.password.id}>パスワード</Field.Label>
          <Input
            data-testid="password-input"
            {...getInputProps(fields.password, { type: "password" })}
            key={fields.password.key}
          />
          <ErrorText>{fields.password.errors}</ErrorText>
        </Field>
        <Button data-testid="login-button" type="submit">
          ログイン
        </Button>
        <div className="text-right">
          <Link asChild>
            <InternalLink href={paths.signup.getHref()}>
              新規登録はこちら
            </InternalLink>
          </Link>
        </div>
      </div>
    </form>
  );
};
