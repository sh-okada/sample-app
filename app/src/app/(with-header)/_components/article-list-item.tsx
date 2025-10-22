import dayjs from "dayjs";
import { Link } from "@/components/core/link";
import { InternalLink } from "@/components/ui-parts/internal-link";
import { paths } from "@/config/paths";

export type Article = {
  id: string;
  title: string;
  text: string;
  publishedAt: Date;
};

export type ArticleListItemProps = {
  article: Article;
};

export const ArticleListItem = ({ article }: ArticleListItemProps) => {
  return (
    <div className="py-2">
      <Link asChild>
        <InternalLink
          data-testid="article-title"
          href={paths.article.id.getHref(article.id)}
        >
          {article.title}
        </InternalLink>
      </Link>
      <p className="text-right">
        {dayjs(article.publishedAt).format("YYYY/MM/DD")} に投稿
      </p>
    </div>
  );
};
