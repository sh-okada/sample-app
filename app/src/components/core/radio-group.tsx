import type { ComponentProps } from "react";

export type RadioGroupProps = ComponentProps<"div">;

export const RadioGroup = ({ className = "", ...props }: RadioGroupProps) => {
  return <div className={`flex gap-2 ${className}`} {...props} />;
};
