import type { ComponentProps, FunctionComponent } from "react";

export const HorizonTalTr = (props: TrProps) => <Tr {...props} />;

export const VerticalTrHeader = ({ className = "", ...rest }: TrProps) => (
  <Tr className={`border-b border-black bg-gray-100 ${className}`} {...rest} />
);

export const VerticalTr: FunctionComponent<TrProps> & {
  Header: typeof VerticalTrHeader;
} = ({ className = "", ...rest }: TrProps) => (
  <Tr className={`border-b border-gray-100 ${className}`} {...rest} />
);

VerticalTr.Header = VerticalTrHeader;

export type TrProps = ComponentProps<"tr">;

export const Tr: FunctionComponent<TrProps> & {
  Horizontal: typeof HorizonTalTr;
  Vertical: typeof VerticalTr;
} = (props: TrProps) => {
  return <tr {...props} />;
};

Tr.Horizontal = HorizonTalTr;
Tr.Vertical = VerticalTr;
