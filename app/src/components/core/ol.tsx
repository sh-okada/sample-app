import type { ComponentProps } from "react";

export const olBaseStyle = "pl-8 list-[revert]";

export type OlProps = ComponentProps<"ol">;

export const Ol = ({ className = "", ...rest }: OlProps) => {
  return <ol className={`${olBaseStyle} ${className}`} {...rest} />;
};
