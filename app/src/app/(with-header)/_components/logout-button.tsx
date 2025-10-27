import { logout } from "@/app/(with-header)/action";
import { Button } from "@/components/core/button";
import { auth } from "@/lib/auth";

export const LogoutButton = async () => {
  const session = await auth();

  return session?.user ? (
    <form action={logout}>
      <Button className="w-full" variant="solid" type="submit">
        ログアウト
      </Button>
    </form>
  ) : null;
};
