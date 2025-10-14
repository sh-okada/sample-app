import { Suspense } from "react";
import { Article } from "@/app/(with-header)/article/[id]/_components/article";
import { Feedback } from "@/app/(with-header)/article/[id]/_components/feedback";
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
          <Article id={id}>
            {(title) => <PageFrame.Title>{title}</PageFrame.Title>}
          </Article>
          <Feedback articleId={id} />
        </Suspense>
      </PageFrame.Content>
    </PageFrame>
  );
}
