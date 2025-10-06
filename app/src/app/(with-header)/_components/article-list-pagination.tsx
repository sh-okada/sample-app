import { getArticleCount } from "@/api/articles";
import { getPaginationProps } from "@/components/core/pagination/helper/getPaginationProps";
import { Pagination } from "@/components/core/pagination/pagination";
import { paths } from "@/config/paths";
import {
  searchArticleParamsCache,
  serializeArticlesParams,
} from "@/lib/nuqs/params";

export const ArticleListPagination = async () => {
  const currentPage = searchArticleParamsCache.get("page");
  const articleCount = (await getArticleCount()).data;

  if (articleCount.count === 0) {
    return null;
  }

  const totalPages = Math.max(1, Math.ceil(articleCount.count / 5));

  return (
    <Pagination
      className="justify-center"
      {...getPaginationProps(currentPage, totalPages, (page: number) =>
        serializeArticlesParams(paths.home.getHref(), {
          ...searchArticleParamsCache.all(),
          page,
        }),
      )}
    />
  );
};
