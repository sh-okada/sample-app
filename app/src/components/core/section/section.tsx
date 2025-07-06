import { SectionContent } from "@/components/core/section/parts/section-content";
import { SectionHeader } from "@/components/core/section/parts/section-header";
import type { ComponentProps, FunctionComponent } from "react";

export type SectionProps = ComponentProps<"section">;

export const Section: FunctionComponent<SectionProps> & {
  Header: typeof SectionHeader;
  Content: typeof SectionContent;
} = ({ ...rest }: SectionProps) => {
  return <section {...rest} />;
};

Section.Header = SectionHeader;
Section.Content = SectionContent;
