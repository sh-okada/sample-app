import { PostArticleForm } from "@/app/(with-header)/article/post/_components/post-article-form";
import { PageFrame } from "@/components/ui-parts/page-frame";
import { paths } from "@/config/paths";

export default function Page() {
  return (
    <PageFrame>
      <PageFrame.Title>{paths.article.post.name}</PageFrame.Title>
      <PageFrame.Content>
        <PostArticleForm />
      </PageFrame.Content>
    </PageFrame>
  );
}
