import type { ReactNode } from "react";
import { MarkdownViewer } from "@/components/ui-parts/markdown-viewer/markdown-viewer";

export type ArticleProps = {
  title: string;
  text: string;
  children: (title: string) => ReactNode;
};

export const Article = ({ title, text, children }: ArticleProps) => {
  return (
    <>
      {children(title)}
      <MarkdownViewer body={text} />
    </>
  );
};
