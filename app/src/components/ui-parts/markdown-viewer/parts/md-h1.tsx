import type { ComponentProps } from "react";

type H1Props = ComponentProps<"h1">;

export const MdH1 = ({ className = "", ...rest }: H1Props) => {
  return <h1 className={`text-[45px] my-4 ${className}`} {...rest} />;
};
