"use client";

import { useEffect } from "react";

export const MswWorker = () => {
  useEffect(() => {
    if (
      process.env.NEXT_PUBLIC_MSW_MOCK !== "enabled" ||
      typeof window === "undefined"
    ) {
      return;
    }

    import("@/lib/msw/browser").then(({ worker }) => {
      worker.start({ onUnhandledRequest: "bypass" });
    });
  });

  return null;
};
