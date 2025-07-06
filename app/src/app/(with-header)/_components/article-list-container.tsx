import { getArticles } from "@/api/articles";
import { ArticleList } from "@/app/(with-header)/_components/article-list";

export type ArticleListContainerProps = {
  page: number;
};

export const ArticleListContainer = async ({
  page,
}: ArticleListContainerProps) => {
  const articles = (await getArticles(page)).data;

  return <ArticleList articles={articles} />;
};
