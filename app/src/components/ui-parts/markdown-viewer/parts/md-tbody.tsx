import type { TbodyProps } from "@/components/core/table/parts/tdoby";
import { Table } from "@/components/core/table/table";

export const MdTbody = (props: TbodyProps) => {
  return <Table.Tbody {...props} />;
};
