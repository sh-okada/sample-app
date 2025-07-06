import { Label } from "@/components/core/label";
import type { ComponentProps, FunctionComponent } from "react";

export type FieldProps = ComponentProps<"div">;

export const Field: FunctionComponent<FieldProps> & { Label: typeof Label } = ({
  className = "",
  ...props
}) => {
  return <div className={`flex flex-col gap-2 ${className}`} {...props} />;
};

Field.Label = Label;
