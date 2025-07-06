import type { ComponentProps } from "react";

type H6Props = ComponentProps<"h6">;

export const MdH6 = ({ className = "", ...rest }: H6Props) => {
  return <h2 className={`text-[24px] ${className}`} {...rest} />;
};
