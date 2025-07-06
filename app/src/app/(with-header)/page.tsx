import { Suspense } from "react";
import { ArticleListContainer } from "@/app/(with-header)/_components/article-list-container";
import { ArticleListPagination } from "@/app/(with-header)/_components/article-list-pagination";
import { PageFrame } from "@/components/ui-parts/page-frame";
import { Spinner } from "@/components/ui-parts/spinner";
import { paths } from "@/config/paths";
import { getArticlesQueryParamsSchema } from "@/lib/zod/schema";

type PageProps = {
  searchParams: Promise<Record<string, string | string[] | undefined>>;
};

export default async function Page({ searchParams }: PageProps) {
  const { page } = await searchParams;
  const parzedQueryParams = await getArticlesQueryParamsSchema.parseAsync({
    page: page,
  });

  return (
    <PageFrame>
      <PageFrame.Title>{paths.home.name}</PageFrame.Title>
      <PageFrame.Content>
        <Suspense key={parzedQueryParams.page} fallback={<Spinner />}>
          <ArticleListContainer page={parzedQueryParams.page ?? 1} />
        </Suspense>
        <ArticleListPagination currentPage={parzedQueryParams.page ?? 1} />
      </PageFrame.Content>
    </PageFrame>
  );
}
