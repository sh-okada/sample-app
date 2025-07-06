import { EditorState, type EditorStateConfig } from "@codemirror/state";
import { EditorView } from "codemirror";
import { useEffect, useRef, useState } from "react";

export type UseCodeMirrorProps = EditorStateConfig & {
  doc?: string;
};

export const useCodeMirror = (props: UseCodeMirrorProps) => {
  const editorRef = useRef(null);
  const [container, setContainer] = useState<HTMLDivElement>();
  const [view, setView] = useState<EditorView>();

  // biome-ignore lint/correctness/useExhaustiveDependencies: <explanation>
  useEffect(() => {
    if (editorRef.current) {
      setContainer(editorRef.current);
    }
  }, [setContainer]);

  useEffect(() => {
    if (!view && container) {
      const state = EditorState.create(props);
      const viewCurrent = new EditorView({
        state,
        parent: container,
      });
      setView(viewCurrent);
    }
  }, [view, container, props]);

  return {
    editorRef,
  };
};
