import type { ReactNode } from "react";
import { Container } from "@/components/ui-parts/container";

export default function WithoutHeaderLayout({
  children,
}: {
  children: ReactNode;
}) {
  return <Container>{children}</Container>;
}
