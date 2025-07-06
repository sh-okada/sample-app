"use client";

import {
  defaultKeymap,
  history,
  historyKeymap,
  indentWithTab,
} from "@codemirror/commands";
import { markdown, markdownLanguage } from "@codemirror/lang-markdown";
import { indentUnit } from "@codemirror/language";
import { keymap, placeholder, type ViewUpdate } from "@codemirror/view";
import { EditorView } from "codemirror";
import { useCodeMirror } from "@/components/ui-parts/markdown-editor/hooks/use-code-mirror";

export type MarkdownEditorProps = {
  doc?: string;
  onChange?: (value: string) => void;
};

export const MarkdownEditor = ({ doc, onChange }: MarkdownEditorProps) => {
  const { editorRef } = useCodeMirror({
    doc: doc,
    extensions: [
      placeholder("# Hello World"),
      history(),
      keymap.of(defaultKeymap),
      keymap.of(historyKeymap),
      keymap.of([indentWithTab]),
      indentUnit.of("    "),
      markdown({
        base: markdownLanguage,
        completeHTMLTags: false,
      }),
      EditorView.theme({
        "&": {
          border: "1px solid #000000",
          borderRadius: "0.375rem",
          fontSize: "16px",
          minHeight: "400px",
        },
        "&.cm-editor": {
          outline: "none",
        },
        "&.cm-focused": {
          outline: "4px solid #000000",
          outlineOffset: "2px",
        },
        ".cm-line": {
          padding: "0px",
        },
        "&:focus-visible": {
          outline: "4px solid #000000",
          outlineOffset: "2px",
        },
        ".cm-content": {
          padding: "12px 16px 12px 16px",
          fontFamily: "Noto Sans JP",
        },
        ".cm-scroller": {
          overflow: "auto",
        },
      }),
      EditorView.updateListener.of((update: ViewUpdate) => {
        if (update.docChanged) {
          onChange?.(update.state.doc.toString());
        }
      }),
    ],
  });

  return <div ref={editorRef} />;
};
