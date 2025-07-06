import { Input, type InputProps } from "@/components/core/input";

export const datePickerBaseStyle = `
  w-full
`;

export type DatePickerProps = Omit<InputProps, "type">;

export const DatePicker = ({ className = "", ...rest }: DatePickerProps) => {
  return (
    <Input
      className={`${datePickerBaseStyle} ${className}`}
      {...rest}
      type="date"
    />
  );
};
