import type { ComponentProps } from "react";

export const ulBaseStyle = "pl-8 list-[revert]";

export type UlProps = ComponentProps<"ul">;

export const Ul = ({ className = "", ...rest }: UlProps) => {
  return <ul className={`${ulBaseStyle} ${className}`} {...rest} />;
};
