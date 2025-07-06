import { Legend, type LegendProps } from "@/components/core/legend";
import type { ComponentProps, FunctionComponent } from "react";

export type FieldsetProps = ComponentProps<"fieldset">;

const FieldsetLegend = ({ className = "", ...rest }: LegendProps) => {
  return <Legend className={`mb-2 ${className}`} {...rest} />;
};

export const Fieldset: FunctionComponent<FieldsetProps> & {
  Legend: typeof FieldsetLegend;
} = ({ className = "", ...rest }: FieldsetProps) => {
  return <fieldset className={`flex flex-col gap-2 ${className}`} {...rest} />;
};

Fieldset.Legend = FieldsetLegend;
