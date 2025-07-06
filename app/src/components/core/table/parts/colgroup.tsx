import type { ComponentProps } from "react";

export type ColgroupProps = ComponentProps<"colgroup">;

export const Colgroup = (props: ColgroupProps) => {
  return <colgroup {...props} />;
};
