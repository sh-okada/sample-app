import { Button } from "@/components/core/button";
import { auth, signOut } from "@/lib/auth";

export const LogoutButton = async () => {
  const session = await auth();

  return session?.user ? (
    <form
      action={async () => {
        "use server";
        await signOut();
      }}
    >
      <Button className="w-full" variant="solid" type="submit">
        ログアウト
      </Button>
    </form>
  ) : null;
};
