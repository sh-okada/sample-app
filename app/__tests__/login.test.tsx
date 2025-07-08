import { fireEvent, render, screen } from "@testing-library/react";
import { LoginForm } from "@/app/(without-header)/login/_components/login-form";
import { describeWithAxiosMock } from "@/lib/jest/describe";

describeWithAxiosMock("ユーザー名とパスワードが正しい場合", (getAxiosMock) => {
  beforeEach(async () => {
    const axiosMock = getAxiosMock();
    axiosMock.onPost("/api/login").reply(200);

    render(<LoginForm />);
    fireEvent.input(screen.getByLabelText("ユーザー名"), {
      target: { value: "user1" },
    });
    fireEvent.input(await screen.getByLabelText("パスワード"), {
      target: { value: "password1" },
    });
    fireEvent.click(await screen.getByRole("button", { name: "ログイン" }));
  });

  test("リダイレクトされること", () => {
    // expect(redirect).toHaveBeenCalled();
  });
});
