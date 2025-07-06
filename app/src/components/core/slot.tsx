import {
  Children,
  cloneElement,
  type HTMLAttributes,
  isValidElement,
  type ReactNode,
} from "react";

export type SlotProps = HTMLAttributes<HTMLElement> & {
  children?: ReactNode;
};

export const Slot = (props: SlotProps) => {
  const { children, ...rest } = props;

  if (isValidElement(children)) {
    // isValidElementでかならずchildrenにはpropsが存在するのでエラーを無視した
    return cloneElement(children, {
      ...rest,
      // @ts-expect-error ts(2698)
      ...children.props,
      // @ts-expect-error ts(18046)
      className: `${rest.className ?? ""} ${children.props.className ?? ""}`,
    });
  }

  if (Children.count(children) > 1) {
    Children.only(null);
  }

  return null;
};
