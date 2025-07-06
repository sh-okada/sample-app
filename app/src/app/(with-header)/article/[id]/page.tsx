import { Suspense } from "react";
import { ArticleContainer } from "@/app/(with-header)/article/[id]/_components/article-container";
import { PageFrame } from "@/components/ui-parts/page-frame";
import { Spinner } from "@/components/ui-parts/spinner";

type PageProps = {
  params: Promise<{ id: string }>;
};

export default async function Page({ params }: PageProps) {
  const { id } = await params;

  return (
    <PageFrame>
      <PageFrame.Content>
        <Suspense fallback={<Spinner />}>
          <ArticleContainer id={id}>
            {(title) => <PageFrame.Title>{title}</PageFrame.Title>}
          </ArticleContainer>
        </Suspense>
      </PageFrame.Content>
    </PageFrame>
  );
}
