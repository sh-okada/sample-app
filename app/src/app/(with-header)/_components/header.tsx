import { ArticleSearchOverlay } from "@/app/(with-header)/_components/article-search-overlay";
import { Brand } from "@/app/(with-header)/_components/brand";
import { HumburgerMenu } from "@/app/(with-header)/_components/humburger-menu";
import { LogoutButton } from "@/app/(with-header)/_components/logout-button";
import { auth } from "@/lib/auth";

export const Header = async () => {
  const session = await auth();

  return (
    <header className="flex justify-between items-center">
      <div className="p-4">
        <Brand />
      </div>
      <div className="flex items-center gap-2">
        <ArticleSearchOverlay />
        <p>{session?.user?.name}</p>
        <HumburgerMenu>
          <LogoutButton />
        </HumburgerMenu>
      </div>
    </header>
  );
};
