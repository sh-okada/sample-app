import { LoginForm } from "@/app/(without-header)/login/_components/login-form";
import { PageFrame } from "@/components/ui-parts/page-frame";
import { paths } from "@/config/paths";

export default function Page() {
  return (
    <PageFrame>
      <PageFrame.Title>{paths.login.name}</PageFrame.Title>
      <PageFrame.Content>
        <LoginForm />
      </PageFrame.Content>
    </PageFrame>
  );
}
