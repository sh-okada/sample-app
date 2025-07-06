import { Link, type LinkProps } from "@/components/core/link";

export const MdLink = (props: LinkProps) => {
  return (
    <Link
      {...props}
      asChild={false}
      target="_blank"
      rel="noopener noreferrer"
    />
  );
};
