import type { ComponentProps } from "react";

export type FullDrawerProps = ComponentProps<"dialog">;

export const FullDrawer = ({ className = "", ...rest }: FullDrawerProps) => {
  return (
    <dialog
      className={`m-[unset] max-w-[unset] max-h-[unset] w-full h-dvh bg-white ${className}`}
      {...rest}
    />
  );
};
