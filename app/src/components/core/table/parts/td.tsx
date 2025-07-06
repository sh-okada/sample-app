import type { ComponentProps } from "react";

export type TdProps = ComponentProps<"td">;

export const Td = ({ className = "", ...rest }: TdProps) => {
  return <td className={`px-4 py-5 align-top ${className}`} {...rest} />;
};
