import type { SearchParams } from "nuqs/server";
import { Suspense } from "react";
import { ArticleList } from "@/app/(with-header)/_components/article-list";
import { PageFrame } from "@/components/ui-parts/page-frame";
import { Spinner } from "@/components/ui-parts/spinner";
import { paths } from "@/config/paths";
import { searchArticleParamsCache } from "@/lib/nuqs/params";

type PageProps = {
  searchParams: Promise<SearchParams>;
};

export default async function Page({ searchParams }: PageProps) {
  const { page, q } = await searchArticleParamsCache.parse(searchParams);

  return (
    <PageFrame>
      <PageFrame.Title>{paths.home.name}</PageFrame.Title>
      <PageFrame.Content>
        <Suspense key={`${page}-${q}`} fallback={<Spinner />}>
          <ArticleList />
        </Suspense>
      </PageFrame.Content>
    </PageFrame>
  );
}
