import type { ComponentProps, FunctionComponent } from "react";
import { FaChevronDown } from "react-icons/fa6";

type SelectItemProps = ComponentProps<"option">;

const SelectItem = (props: SelectItemProps) => {
  return <option {...props} />;
};

export type SelectItems<T> = { value: T; label: string }[];

export const selectBaseStyle = `
  w-full
  appearance-none
  border
  border-black
  rounded-md
  px-4 py-3
  focus-visible:outline focus-visible:outline-4 focus-visible:outline-black focus-visible:outline-offset-2
  disabled:pointer-events-none disabled:text-gray-500 disabled:bg-gray-300 disabled:border-none
  aria-[invalid=true]:border-red-900
`;

export type SelectProps = ComponentProps<"select"> & {
  isError?: boolean;
};

export const Select: FunctionComponent<SelectProps> & {
  Item: typeof SelectItem;
} = ({ isError, className = "", ...rest }: SelectProps) => {
  return (
    <span className="relative">
      <select
        className={`${selectBaseStyle} ${className}`}
        aria-invalid={isError || undefined}
        {...rest}
      />
      <FaChevronDown
        className={`absolute right-4 top-1/2 -translate-y-1/2 ${rest.disabled ? "text-gray-500" : "text-black"}`}
      />
    </span>
  );
};

Select.Item = SelectItem;
