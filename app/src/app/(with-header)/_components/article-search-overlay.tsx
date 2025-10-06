"use client";

import { usePathname } from "next/navigation";
import { useEffect, useRef } from "react";
import { FaMagnifyingGlass, FaXmark } from "react-icons/fa6";

import { ArticleSearchForm } from "@/app/(with-header)/_components/article-search-form";
import { Button } from "@/components/core/button";
import { FullDrawer } from "@/components/core/drawer/full-drawer";
import { Container } from "@/components/ui-parts/container";

export const ArticleSearchOverlay = () => {
  const drawerRef = useRef<HTMLDialogElement>(null);
  const pathname = usePathname();

  // biome-ignore lint/correctness/useExhaustiveDependencies: <explanation>
  useEffect(() => {
    drawerRef.current?.close();
  }, [pathname]);

  return (
    <>
      <div className="p-4">
        <Button
          variant="text"
          type="button"
          onClick={() => drawerRef.current?.showModal()}
        >
          <FaMagnifyingGlass />
        </Button>
      </div>
      <FullDrawer ref={drawerRef}>
        <div className="flex justify-end p-4">
          <Button
            variant="text"
            type="button"
            onClick={() => drawerRef.current?.close()}
          >
            <FaXmark />
          </Button>
        </div>
        <Container>
          <ArticleSearchForm />
        </Container>
      </FullDrawer>
    </>
  );
};
