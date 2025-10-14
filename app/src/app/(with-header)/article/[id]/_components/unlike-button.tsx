"use client";

import { getFormProps, getInputProps, useForm } from "@conform-to/react";
import { useActionState } from "react";
import { FaRegHeart } from "react-icons/fa6";
import { unlike } from "@/app/(with-header)/article/[id]/action";
import { Button } from "@/components/core/button";
import { Input } from "@/components/core/input";

export type UnLikeButtonProps = {
  articleId: string;
};

export const UnLikeButton = ({ articleId }: UnLikeButtonProps) => {
  const [_lastResult, action] = useActionState(unlike, null);
  const [form, fields] = useForm({
    defaultValue: { articleId },
  });

  return (
    <form {...getFormProps(form)} action={action}>
      <Input
        {...getInputProps(fields.articleId, { type: "hidden" })}
        key={fields.articleId.key}
      />
      <Button className="text-[24px]" variant="text" type="submit">
        <FaRegHeart />
      </Button>
    </form>
  );
};
