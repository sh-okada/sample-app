import type { ComponentProps } from "react";

export type SectionContentProps = ComponentProps<"div">;

export const SectionContent = ({
  className = "",
  ...rest
}: SectionContentProps) => {
  return <div className={`mt-2 ${className}`} {...rest} />;
};
