import { Slot } from "@/components/core/slot";
import type { ComponentProps } from "react";

export const linkStyle = `
  text-blue-900
  rounded-md
  underline
  hover:decoration-2
  focus-visible:outline focus-visible:outline-4 focus-visible:outline-black focus-visible:outline-offset-2
`;

export type LinkProps = { className?: string } & (
  | ({ asChild?: false } & ComponentProps<"a">)
  | { asChild: true; children: React.ReactNode }
);

export const Link = ({
  asChild,
  children,
  className = "",
  ...rest
}: LinkProps) => {
  if (asChild) {
    return (
      <Slot className={`${linkStyle} ${className}`} {...rest}>
        {children}
      </Slot>
    );
  }

  return (
    <a className={`${linkStyle} ${className}`} {...rest}>
      {children}
    </a>
  );
};
