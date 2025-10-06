"use client";

import { usePathname } from "next/navigation";
import { type ReactNode, useEffect, useRef } from "react";
import { FaBars, FaXmark } from "react-icons/fa6";
import { Button } from "@/components/core/button";
import { FullDrawer } from "@/components/core/drawer/full-drawer";
import { Container } from "@/components/ui-parts/container";
import { InternalLink } from "@/components/ui-parts/internal-link";
import { paths } from "@/config/paths";

const menuItems = [
  {
    key: 1,
    label: paths.home.name,
    url: paths.home.getHref(),
  },
  {
    key: 2,
    label: paths.article.post.name,
    url: paths.article.post.getHref(),
  },
];

export type HumburgerMenuProps = {
  children: ReactNode;
};

export const HumburgerMenu = ({ children }: HumburgerMenuProps) => {
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
          <FaBars />
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
        <Container className="flex flex-col gap-4">
          {menuItems.map((menuItem) => (
            <Button key={menuItem.key} variant="text" asChild>
              <InternalLink href={menuItem.url}>{menuItem.label}</InternalLink>
            </Button>
          ))}
          {children}
        </Container>
      </FullDrawer>
    </>
  );
};
