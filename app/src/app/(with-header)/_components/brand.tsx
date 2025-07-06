import { InternalLink } from "@/components/ui-parts/internal-link";
import { paths } from "@/config/paths";

export const Brand = () => {
  return (
    <InternalLink href={paths.home.getHref({})}>サンプルアプリ</InternalLink>
  );
};
