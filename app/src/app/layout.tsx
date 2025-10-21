import type { Metadata } from "next";
import "./globals.css";
import { Noto_Sans_JP } from "next/font/google";
import { headers } from "next/headers";
import type { ReactNode } from "react";

if (
  process.env.NEXT_RUNTIME === "nodejs" &&
  process.env.NODE_ENV !== "production" &&
  process.env.ENABLE_REQUEST_MOCKING === "true"
) {
  const { setupFetchInterceptor } = await import(
    "request-mocking-protocol/fetch"
  );
  setupFetchInterceptor(() => headers());
}

const notoSans = Noto_Sans_JP({
  weight: ["400", "500", "700"],
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Next.js + FastAPI サンプルアプリ",
  description: "Next.js + FastAPI サンプルアプリです。",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ja" className={notoSans.className}>
      <body>{children}</body>
    </html>
  );
}
