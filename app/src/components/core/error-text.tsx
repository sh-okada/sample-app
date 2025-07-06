import type { ComponentProps } from "react";

export type ErrorTextProps = ComponentProps<"p">;

export const ErrorText = ({ className = "", ...props }: ErrorTextProps) => {
  return <p className={`text-red-500 ${className}`} {...props} />;
};
