import type { PaginationProps } from "@/components/core/pagination/pagination";

export const getPaginationProps = (
  currentPage: number,
  totalPages: number,
  getUrl: (page: number) => string,
): PaginationProps => {
  const topUrl = getUrl(1);
  const lastUrl = getUrl(totalPages);
  const prevUrl = getUrl(currentPage === 1 ? currentPage : currentPage - 1);
  const nextUrl = getUrl(
    currentPage === totalPages ? totalPages : currentPage + 1,
  );

  return {
    currentPage,
    totalPages,
    topUrl,
    lastUrl,
    prevUrl,
    nextUrl,
  };
};
