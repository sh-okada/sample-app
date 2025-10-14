import { Like } from "@/app/(with-header)/article/[id]/_components/like";

export type FeedbackProps = {
  articleId: string;
};

export const Feedback = ({ articleId }: FeedbackProps) => {
  return (
    <div className="flex gap-2 justify-end">
      <Like articleId={articleId} />
    </div>
  );
};
