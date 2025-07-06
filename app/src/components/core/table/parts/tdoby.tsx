import type { ComponentProps } from "react";

export type TbodyProps = ComponentProps<"tbody">;

export const Tbody = (props: TbodyProps) => {
  return <tbody {...props} />;
};
