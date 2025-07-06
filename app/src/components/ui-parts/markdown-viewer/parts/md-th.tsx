import type { ThProps } from "@/components/core/table/parts/th";
import { Table } from "@/components/core/table/table";

export const MdTh = ({ className = "", ...rest }: ThProps) => {
  return (
    <Table.Th.Vertical
      className={`border-b border-black bg-gray-100 ${className}`}
      {...rest}
    />
  );
};
