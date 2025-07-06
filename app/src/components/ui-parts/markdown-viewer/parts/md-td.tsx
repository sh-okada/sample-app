import type { TdProps } from "@/components/core/table/parts/td";
import { Table } from "@/components/core/table/table";

export const MdTd = (props: TdProps) => {
  return <Table.Td {...props} />;
};
