import type { TrProps } from "@/components/core/table/parts/tr";
import { Table } from "@/components/core/table/table";

export const MdTr = (props: TrProps) => {
  return <Table.Tr.Vertical {...props} />;
};
