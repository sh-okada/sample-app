import type { ComponentProps, FunctionComponent, ReactNode } from "react";

type PageTitleProps = ComponentProps<"h1">;

const PageTitle = ({ className = "", ...rest }: PageTitleProps) => (
  <h1 className={`text-[45px] mb-8 ${className}`} {...rest} />
);

type PageContentProps = {
  children: ReactNode;
};

const PageContent = ({ children }: PageContentProps) => <>{children}</>;

export type PageFrameProps = {
  children?: ReactNode;
};

export const PageFrame: FunctionComponent<PageFrameProps> & {
  Title: typeof PageTitle;
  Content: typeof PageContent;
} = ({ children }: PageFrameProps) => {
  return <main>{children}</main>;
};

PageFrame.Title = PageTitle;
PageFrame.Content = PageContent;
