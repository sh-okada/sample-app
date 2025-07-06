import {
  type Article,
  ArticleListItem,
} from "@/app/(with-header)/_components/article-list-item";

export type ArticleListProps = {
  articles: Article[];
};

export const ArticleList = ({ articles }: ArticleListProps) => {
  if (articles.length === 0) {
    <p className="text-center">記事は投稿されていません</p>;
  }

  return (
    <>
      {articles.map((article) => (
        <ArticleListItem key={article.id} article={article} />
      ))}
    </>
  );
};
