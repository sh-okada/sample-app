import type { TheadProps } from "@/components/core/table/parts/thead";
import { Table } from "@/components/core/table/table";

export const MdThead = (props: TheadProps) => {
  return <Table.Thead {...props} />;
};
