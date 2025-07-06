import type { ComponentProps } from "react";

const inputBaseStyle = `
  border
  border-black
  rounded-md
  px-4 py-3
  focus-visible:outline focus-visible:outline-4 focus-visible:outline-black focus-visible:outline-offset-2
  disabled:pointer-events-none disabled:text-gray-500 disabled:bg-gray-300 disabled:border-none
  aria-[invalid=true]:border-red-900
`;

export type InputProps = ComponentProps<"input"> & {
  isError?: boolean;
};

export const Input = ({ isError, className = "", ...rest }: InputProps) => {
  return (
    <input
      className={`${inputBaseStyle} ${className}`}
      aria-invalid={isError || undefined}
      {...rest}
    />
  );
};
