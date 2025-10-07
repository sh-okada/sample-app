import { getArticles } from "@/api/articles";
import {
  type Article,
  ArticleListItem,
} from "@/app/(with-header)/_components/article-list-item";
import { getPaginationProps } from "@/components/core/pagination/helper/getPaginationProps";
import { Pagination } from "@/components/core/pagination/pagination";
import { paths } from "@/config/paths";
import {
  searchArticleParamsCache,
  serializeArticlesParams,
} from "@/lib/nuqs/params";

export type ArticleListProps = {
  articles: Article[];
};

export const ArticleList = async () => {
  const { page, q } = searchArticleParamsCache.all();
  const articles = (await getArticles(page, q)).data;

  const totalPages = Math.max(1, Math.ceil(articles.count / 5));

  if (articles.count === 0) {
    return <p className="text-center">記事は投稿されていません</p>;
  }

  return (
    <>
      {articles.values.map((article) => (
        <ArticleListItem key={article.id} article={article} />
      ))}
      <Pagination
        className="justify-center"
        {...getPaginationProps(page, totalPages, (page: number) =>
          serializeArticlesParams(paths.home.getHref(), {
            ...searchArticleParamsCache.all(),
            page,
          }),
        )}
      />
    </>
  );
};
