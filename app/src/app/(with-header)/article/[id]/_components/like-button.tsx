"use client";

import { getFormProps, getInputProps, useForm } from "@conform-to/react";
import { useActionState } from "react";
import { FaHeart } from "react-icons/fa6";
import { like } from "@/app/(with-header)/article/[id]/action";
import { Button } from "@/components/core/button";
import { Input } from "@/components/core/input";

export type LikeButtonProps = {
  articleId: string;
};

export const LikeButton = ({ articleId }: LikeButtonProps) => {
  const [_lastResult, action] = useActionState(like, null);
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
        <FaHeart />
      </Button>
    </form>
  );
};
