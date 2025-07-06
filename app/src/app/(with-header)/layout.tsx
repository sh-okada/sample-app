import type { ReactNode } from "react";
import { Header } from "@/app/(with-header)/_components/header";
import { Container } from "@/components/ui-parts/container";

export default function WithHeaderLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <>
      <Header />
      <Container>{children}</Container>
    </>
  );
}
