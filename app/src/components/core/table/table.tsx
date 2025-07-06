import { Col } from "@/components/core/table/parts/col";
import { Colgroup } from "@/components/core/table/parts/colgroup";
import { Td } from "@/components/core/table/parts/td";
import { Tbody } from "@/components/core/table/parts/tdoby";
import { Th } from "@/components/core/table/parts/th";
import { Thead } from "@/components/core/table/parts/thead";
import { Tr } from "@/components/core/table/parts/tr";
import type { ComponentProps, FunctionComponent } from "react";

export type TableProps = ComponentProps<"table">;

export const Table: FunctionComponent<TableProps> & {
  Colgroup: typeof Colgroup;
  Col: typeof Col;
  Thead: typeof Thead;
  Tbody: typeof Tbody;
  Tr: typeof Tr;
  Th: typeof Th;
  Td: typeof Td;
} = (props: TableProps) => {
  return <table {...props} />;
};

Table.Colgroup = Colgroup;
Table.Col = Col;
Table.Thead = Thead;
Table.Tbody = Tbody;
Table.Tr = Tr;
Table.Th = Th;
Table.Td = Td;
