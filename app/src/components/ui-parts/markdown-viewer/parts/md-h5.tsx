import type { ComponentProps } from "react";

type H5Props = ComponentProps<"h5">;

export const MdH5 = ({ className = "", ...rest }: H5Props) => {
  return <h5 className={`text-[26px] ${className}`} {...rest} />;
};
