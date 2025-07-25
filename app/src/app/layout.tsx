import type { Metadata } from "next";
import "./globals.css";
import { Noto_Sans_JP } from "next/font/google";
import type { ReactNode } from "react";

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
