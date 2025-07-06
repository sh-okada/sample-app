"use client";

import { ClipBordButton } from "@/components/ui-parts/markdown/parts/clip-bord-button";
import type { ComponentProps } from "react";
import { FaClipboard } from "react-icons/fa6";
import { FaClipboardCheck } from "react-icons/fa6";

import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";

export type MdCodeBlockProps = ComponentProps<"code"> & {
  inline?: boolean;
};

export const MdCodeBlock = ({
  inline = false,
  className,
  children,
}: MdCodeBlockProps) => {
  if (inline) {
    return <code className={className}>{children}</code>;
  }

  const match = /language-(\w+)/.exec(className || "");
  if (!match) {
    return <code className={className}>{children}</code>;
  }

  const lang = match[1] ?? undefined;
  const text = String(children).replace(/\n$/, "");

  return (
    <div className="relative">
      <SyntaxHighlighter style={vscDarkPlus} language={lang}>
        {text}
      </SyntaxHighlighter>
      <ClipBordButton className="absolute top-1 right-1" text={text}>
        {(cliped) => (cliped ? <FaClipboardCheck /> : <FaClipboard />)}
      </ClipBordButton>
    </div>
  );
};
