import type { ComponentProps, FunctionComponent } from "react";

export const HorizontalThCol = () => (
  <Col className="border-r border-black bg-gray-100" />
);

export const HorizontalTdCol = () => (
  <Col className="border-r border-gray-100" />
);

export type ColProps = ComponentProps<"col">;

export const Col: FunctionComponent<ColProps> & {
  HorizontalTh: typeof HorizontalThCol;
  HorizontalTd: typeof HorizontalTdCol;
} = (props: ColProps) => {
  return <col {...props} />;
};

Col.HorizontalTh = HorizontalThCol;
Col.HorizontalTd = HorizontalTdCol;
