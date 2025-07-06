import type { ReactNode } from "react";
import { getArticle } from "@/api/articles";
import { Article } from "@/app/(with-header)/article/[id]/_components/article";

export type ArticleContainerProps = {
  id: string;
  children: (title: string) => ReactNode;
};

export const ArticleContainer = async ({
  id,
  children,
}: ArticleContainerProps) => {
  const article = (await getArticle(id)).data;

  return (
    <Article title={article.title} text={article.text}>
      {(title) => children(title)}
    </Article>
  );
};
