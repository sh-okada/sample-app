import type { ComponentProps } from "react";

type H2Props = ComponentProps<"h2">;

export const MdH2 = ({ className = "", ...rest }: H2Props) => {
  return <h2 className={`text-[36px] my-4 ${className}`} {...rest} />;
};
