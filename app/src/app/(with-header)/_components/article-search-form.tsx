"use client";

import { getFormProps, getInputProps, useForm } from "@conform-to/react";
import { parseWithZod } from "@conform-to/zod";
import { useActionState } from "react";
import { searchArticle } from "@/app/(with-header)/action";
import { ErrorText } from "@/components/core/error-text";
import { Field } from "@/components/core/field";
import { Input } from "@/components/core/input";
import { searchArticleSchema } from "@/lib/zod/schema";

export const ArticleSearchForm = () => {
  const [lastResult, action] = useActionState(searchArticle, null);
  const [form, fields] = useForm({
    lastResult,
    onValidate({ formData }) {
      return parseWithZod(formData, { schema: searchArticleSchema });
    },
    shouldValidate: "onSubmit",
  });

  return (
    <form {...getFormProps(form)} action={action}>
      <Field>
        <Field.Label htmlFor={fields.q.id}>検索ワード</Field.Label>
        <Input
          className="w-full"
          placeholder="React"
          {...getInputProps(fields.q, { type: "search" })}
          key={fields.q.key}
        />
        <ErrorText>{fields.q.errors}</ErrorText>
      </Field>
    </form>
  );
};
