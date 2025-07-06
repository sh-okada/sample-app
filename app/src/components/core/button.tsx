import { Slot } from "@/components/core/slot";
import type { ComponentProps } from "react";

export type ButtonVariant = "solid" | "outline" | "text";

const buttonVariantStyle: { [key in ButtonVariant]: string } = {
  solid: `
    text-white
    bg-blue-800
    hover:bg-blue-900 hover:underline
    disabled:text-gray-500 disabled:bg-gray-300
	`,
  outline: `
    text-blue-900
    border border-blue-800
    hover:bg-blue-50 hover:underline
    disabled:text-gray-500  disabled:border-gray-300
	`,
  text: `
    underline
    text-blue-900
    hover:decoration-2 hover:bg-blue-50
    disabled:text-gray-500
	`,
};

const buttonBaseStyle = `
  cursor-pointer
  px-4 py-3
  rounded-md
  focus-visible:outline focus-visible:outline-4 focus-visible:outline-black focus-visible:outline-offset-2
  disabled:pointer-events-none
`;

export type ButtonProps = { className?: string; variant?: ButtonVariant } & (
  | ({ asChild?: false } & ComponentProps<"button">)
  | { asChild: true; children: React.ReactNode }
);

export const Button = ({
  variant = "solid",
  className = "",
  asChild,
  children,
  ...rest
}: ButtonProps) => {
  if (asChild) {
    return (
      <Slot
        className={`${buttonBaseStyle} ${buttonVariantStyle[variant]} ${className}`}
        {...rest}
      >
        {children}
      </Slot>
    );
  }

  return (
    <button
      className={`${buttonBaseStyle} ${buttonVariantStyle[variant]} ${className}`}
      {...rest}
    >
      {children}
    </button>
  );
};
