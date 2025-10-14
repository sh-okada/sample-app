import { getArticle } from "@/api/articles";
import { getLikedArticle } from "@/api/users";
import { LikeButton } from "@/app/(with-header)/article/[id]/_components/like-button";
import { UnlikeButton } from "@/app/(with-header)/article/[id]/_components/unlike-button";
import { auth } from "@/lib/auth";
import { isNotFoundError } from "@/lib/axios";

export type LikeProps = {
  articleId: string;
};

export const Like = async ({ articleId }: LikeProps) => {
  const session = await auth();
  if (!session?.user) {
    return null;
  }

  const article = (await getArticle(articleId)).data;
  if (article.user.id === session.user.id) {
    return null;
  }

  const liked = await getLikedArticle(articleId)
    .then(() => true)
    .catch((error) => {
      if (isNotFoundError(error)) {
        return false;
      }

      return Promise.reject(error);
    });

  return liked ? (
    <UnlikeButton articleId={articleId} />
  ) : (
    <LikeButton articleId={articleId} />
  );
};
