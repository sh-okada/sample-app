import { StepperHeader } from "@/components/core/stepper/parts/stepper-header";
import { StepperProgress } from "@/components/core/stepper/parts/stepper-progress";
import type { ComponentProps, FunctionComponent } from "react";

export type StepperProps = ComponentProps<"div">;

export const Stepper: FunctionComponent<StepperProps> & {
  Progress: typeof StepperProgress;
  Header: typeof StepperHeader;
} = ({ className = "", ...rest }: StepperProps) => {
  return <div className={`flex gap-4 items-center ${className}`} {...rest} />;
};

Stepper.Progress = StepperProgress;
Stepper.Header = StepperHeader;
