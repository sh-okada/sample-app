import type { ComponentProps } from "react";

type H4Props = ComponentProps<"h4">;

export const MdH4 = ({ className = "", ...rest }: H4Props) => {
  return <h4 className={`text-[28px] ${className}`} {...rest} />;
};
