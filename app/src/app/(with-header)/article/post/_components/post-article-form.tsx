"use client";

import {
  getFormProps,
  getInputProps,
  useForm,
  useInputControl,
} from "@conform-to/react";
import { parseWithZod } from "@conform-to/zod";
import { useActionState } from "react";
import { postArticle } from "@/app/(with-header)/article/post/action";
import { Button } from "@/components/core/button";
import { ErrorText } from "@/components/core/error-text";
import { Field } from "@/components/core/field";
import { Fieldset } from "@/components/core/fieldset";
import { Input } from "@/components/core/input";
import { MarkdownEditor } from "@/components/ui-parts/markdown-editor/markdown-editor";
import { postArticleSchema } from "@/lib/zod/schema";

export const PostArticleForm = () => {
  const [lastResult, action] = useActionState(postArticle, null);
  const [form, fields] = useForm({
    lastResult,
    onValidate({ formData }) {
      return parseWithZod(formData, { schema: postArticleSchema });
    },
    shouldValidate: "onBlur",
  });
  const text = useInputControl(fields.text);

  return (
    <form
      className="flex flex-col gap-8"
      {...getFormProps(form)}
      action={action}
    >
      <Field>
        <Field.Label htmlFor={fields.title.id}>タイトル</Field.Label>
        <Input
          data-testid="article-title-input"
          placeholder="例）イケてるコードとは？"
          {...getInputProps(fields.title, { type: "text" })}
          key={fields.title.key}
        />
        <ErrorText data-testid="article-title-error-text">
          {fields.title.errors}
        </ErrorText>
      </Field>
      <Fieldset>
        <Fieldset.Legend>内容</Fieldset.Legend>
        <MarkdownEditor
          data-testid="article-text-input"
          doc={text.value}
          onChange={text.change}
        />
      </Fieldset>
      <Button data-testid="post-article-button" type="submit">
        投稿
      </Button>
    </form>
  );
};
