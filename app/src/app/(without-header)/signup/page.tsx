import { SignUpForm } from "@/app/(without-header)/signup/_components/signup-form";
import { PageFrame } from "@/components/ui-parts/page-frame";
import { paths } from "@/config/paths";

export default function Page() {
  return (
    <PageFrame>
      <PageFrame.Title>{paths.signup.name}</PageFrame.Title>
      <PageFrame.Content>
        <SignUpForm />
      </PageFrame.Content>
    </PageFrame>
  );
}
