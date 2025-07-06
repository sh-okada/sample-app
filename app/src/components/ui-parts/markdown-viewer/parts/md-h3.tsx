import type { ComponentProps } from "react";

type H3Props = ComponentProps<"h3">;

export const MdH3 = ({ className = "", ...rest }: H3Props) => {
  return <h3 className={`text-[32px] my-4 ${className}`} {...rest} />;
};
