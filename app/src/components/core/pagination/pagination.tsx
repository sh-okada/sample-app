import type { ComponentProps } from "react";
import {
  FaAngleLeft,
  FaAngleRight,
  FaAnglesLeft,
  FaAnglesRight,
} from "react-icons/fa6";
import { Button } from "@/components/core/button";
import { InternalLink } from "@/components/ui-parts/internal-link";

export type PaginationProps = ComponentProps<"nav"> & {
  currentPage: number;
  totalPages: number;
  topUrl: string;
  lastUrl: string;
  prevUrl: string;
  nextUrl: string;
};

export const Pagination = ({
  currentPage,
  totalPages,
  topUrl,
  lastUrl,
  prevUrl,
  nextUrl,
  className = "",
  ...rest
}: PaginationProps) => {
  return (
    <nav className={`flex items-center gap-2 ${className}`} {...rest}>
      <div className="flex">
        <Button data-testid="first-page-button" variant="text" asChild>
          <InternalLink href={topUrl}>
            <FaAnglesLeft />
          </InternalLink>
        </Button>
        <Button data-testid="prev-page-button" variant="text" asChild>
          <InternalLink href={prevUrl}>
            <FaAngleLeft />
          </InternalLink>
        </Button>
      </div>
      <p data-testid="current-page">
        {currentPage}/{totalPages}
      </p>
      <div className="flex">
        <Button data-testid="next-page-button" variant="text" asChild>
          <InternalLink href={nextUrl}>
            <FaAngleRight />
          </InternalLink>
        </Button>
        <Button data-testid="last-page-button" variant="text" asChild>
          <InternalLink href={lastUrl}>
            <FaAnglesRight />
          </InternalLink>
        </Button>
      </div>
    </nav>
  );
};
