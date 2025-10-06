import type { ReactNode } from "react";
import { getArticle } from "@/api/articles";
import { MarkdownViewer } from "@/components/ui-parts/markdown-viewer/markdown-viewer";

export type ArticleProps = {
  id: string;
  children: (title: string) => ReactNode;
};

export const Article = async ({ id, children }: ArticleProps) => {
  const article = (await getArticle(id)).data;
  return (
    <>
      {children(article.title)}
      <MarkdownViewer body={article.text} />
    </>
  );
};
