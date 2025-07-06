import type { ComponentProps, FunctionComponent } from "react";

export const HorizonTalTh = ({ className = "", ...rest }: ThProps) => (
  <Th
    className={`px-4 py-5 text-start align-top ${className}`}
    scope="row"
    {...rest}
  />
);

export const VerticalTh = ({ className = "", ...rest }: ThProps) => (
  <Th
    className={`px-4 py-5 text-start align-top ${className}`}
    scope="col"
    {...rest}
  />
);

export type ThProps = ComponentProps<"th">;

export const Th: FunctionComponent<ThProps> & {
  Horizontal: typeof HorizonTalTh;
  Vertical: typeof VerticalTh;
} = (props: ThProps) => {
  return <th {...props} />;
};

Th.Horizontal = HorizonTalTh;
Th.Vertical = VerticalTh;
