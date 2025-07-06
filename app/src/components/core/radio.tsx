import { Label } from "@/components/core/label";
import type { ComponentProps } from "react";

export const radioBaseStyle = `
  appearance-none
  size-4
  rounded-full
  border border-black
  checked:border-blue-900 checked:before:bg-blue-900
  before:hidden before:size-full before:bg-white before:[clip-path:circle(calc(5/16*100%))]
    checked:before:block
  focus-visible:outline focus-visible:outline-4 focus-visible:outline-black focus-visible:outline-offset-2
  disabled:border-gray-500 disabled:bg-gray-300 disabled:checked:border-gray-500 disabled:before:bg-gray-500
  aria-[invalid=true]:checked:border-red-900 aria-[invalid=true]:before:bg-red-900
`;

export type RadioProps = Omit<ComponentProps<"input">, "type"> & {
  isError?: boolean;
};

export const Radio = ({
  isError,
  children,
  className = "",
  ...rest
}: RadioProps) => {
  return (
    <Label className="flex items-center gap-2">
      <input
        className={`${radioBaseStyle} ${className}`}
        type="radio"
        aria-invalid={isError || undefined}
        {...rest}
      />
      <span>{children}</span>
    </Label>
  );
};
