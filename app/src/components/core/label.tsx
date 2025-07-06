import type { ComponentProps } from "react";

export type LabelProps = ComponentProps<"label">;

export const Label = (props: LabelProps) => {
  // biome-ignore lint/a11y/noLabelWithoutControl: <explanation>
  return <label {...props} />;
};
