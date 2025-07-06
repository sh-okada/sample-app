import ReactMarkdown from "react-markdown";
import remarkBreaks from "remark-breaks";
import remarkGfm from "remark-gfm";
import { MdCheckbox } from "@/components/ui-parts/markdown-viewer/parts/md-checkbox";
import { MdCodeBlock } from "@/components/ui-parts/markdown-viewer/parts/md-code-block";
import { MdH1 } from "@/components/ui-parts/markdown-viewer/parts/md-h1";
import { MdH2 } from "@/components/ui-parts/markdown-viewer/parts/md-h2";
import { MdH3 } from "@/components/ui-parts/markdown-viewer/parts/md-h3";
import { MdH4 } from "@/components/ui-parts/markdown-viewer/parts/md-h4";
import { MdH5 } from "@/components/ui-parts/markdown-viewer/parts/md-h5";
import { MdH6 } from "@/components/ui-parts/markdown-viewer/parts/md-h6";
import { MdLink } from "@/components/ui-parts/markdown-viewer/parts/md-link";
import { MdOl } from "@/components/ui-parts/markdown-viewer/parts/md-ol";
import { MdTable } from "@/components/ui-parts/markdown-viewer/parts/md-table";
import { MdTbody } from "@/components/ui-parts/markdown-viewer/parts/md-tbody";
import { MdTd } from "@/components/ui-parts/markdown-viewer/parts/md-td";
import { MdTh } from "@/components/ui-parts/markdown-viewer/parts/md-th";
import { MdThead } from "@/components/ui-parts/markdown-viewer/parts/md-thead";
import { MdTr } from "@/components/ui-parts/markdown-viewer/parts/md-tr";
import { MdUl } from "@/components/ui-parts/markdown-viewer/parts/md-ul";

export type MarkdownViewerProps = {
  body?: string;
};

export const MarkdownViewer = ({ body }: MarkdownViewerProps) => {
  return (
    <ReactMarkdown
      components={{
        h1: MdH1,
        h2: MdH2,
        h3: MdH3,
        h4: MdH4,
        h5: MdH5,
        h6: MdH6,
        a: MdLink,
        ul: MdUl,
        ol: MdOl,
        code: MdCodeBlock,
        table: MdTable,
        thead: MdThead,
        tbody: MdTbody,
        tr: MdTr,
        th: MdTh,
        td: MdTd,
        input: ({ checked, ...props }) => {
          if (props.type === "checkbox") {
            return <MdCheckbox checked={checked} {...props} />;
          }
        },
      }}
      remarkPlugins={[remarkGfm, remarkBreaks]}
    >
      {body}
    </ReactMarkdown>
  );
};
