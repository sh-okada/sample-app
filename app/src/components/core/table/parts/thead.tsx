import type { ComponentProps } from "react";

export type TheadProps = ComponentProps<"thead">;

export const Thead = (props: TheadProps) => {
  return <thead {...props} />;
};
