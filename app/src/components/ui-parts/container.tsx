import type { ComponentProps } from "react";

export type ContainerProps = ComponentProps<"div">;

export const Container = ({ className = "", ...rest }: ContainerProps) => {
  return <div className={`max-w-3xl m-auto p-4 ${className}`} {...rest} />;
};
