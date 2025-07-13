"use client";

import { Button } from "@/components/core/button";

export default function ErrorPage({
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="text-center p-4">
      <h2 className="mb-4">予期しないエラーが発生しました。</h2>
      <Button type="button" onClick={() => reset()}>
        もう一度試す
      </Button>
    </div>
  );
}
