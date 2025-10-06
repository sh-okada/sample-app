import { getArticles } from "@/api/articles";
import {
  type Article,
  ArticleListItem,
} from "@/app/(with-header)/_components/article-list-item";
import { searchArticleParamsCache } from "@/lib/nuqs/params";

export type ArticleListProps = {
  articles: Article[];
};

export const ArticleList = async () => {
  const { page, q } = searchArticleParamsCache.all();
  const articles = (await getArticles(page, q)).data;

  if (articles.length === 0) {
    return <p className="text-center">記事は投稿されていません</p>;
  }

  return (
    <>
      {articles.map((article) => (
        <ArticleListItem key={article.id} article={article} />
      ))}
    </>
  );
};
