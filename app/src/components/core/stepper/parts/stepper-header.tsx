import type { ComponentProps } from "react";

export type SteppterHeaderProps = ComponentProps<"h2">;

export const StepperHeader = ({
  className = "",
  ...rest
}: SteppterHeaderProps) => {
  return <h2 className={`text-xl ${className}`} {...rest} />;
};
