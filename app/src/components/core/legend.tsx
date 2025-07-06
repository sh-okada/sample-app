import type { ComponentProps } from "react";

export type LegendProps = ComponentProps<"legend">;

export const Legend = (props: LegendProps) => {
  return <legend {...props} />;
};
