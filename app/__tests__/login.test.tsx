import { fireEvent, render, screen } from "@testing-library/react";
import { redirect } from "next/navigation";
import { LoginForm } from "@/app/(without-header)/login/_components/login-form";
import { signIn } from "@/lib/auth";
import { describeWithAxiosMock, throwAuthError } from "@/lib/jest/util";

describeWithAxiosMock("ユーザー名とパスワードが正しい場合", (getAxiosMock) => {
  beforeEach(() => {
    const axiosMock = getAxiosMock();
    axiosMock.onPost("/api/login").reply(200);

    render(<LoginForm />);
    fireEvent.input(screen.getByLabelText("ユーザー名"), {
      target: { value: "user1" },
    });
    fireEvent.input(screen.getByLabelText("パスワード"), {
      target: { value: "password" },
    });
    fireEvent.click(screen.getByRole("button", { name: "ログイン" }));
  });

  test("リダイレクトされること", () => {
    expect(redirect).toHaveBeenCalled();
  });
});

describeWithAxiosMock(
  "ユーザー名とパスワードが正しくない場合",
  (_getAxiosMock) => {
    beforeEach(() => {
      throwAuthError(signIn as jest.Mock, new Error());

      render(<LoginForm />);
      fireEvent.input(screen.getByLabelText("ユーザー名"), {
        target: { value: "user1" },
      });
      fireEvent.input(screen.getByLabelText("パスワード"), {
        target: { value: "password" },
      });
      fireEvent.click(screen.getByRole("button", { name: "ログイン" }));
    });

    test("「ユーザー名またはパスワードが間違っています」が表示されること", () => {
      expect(
        screen.getByText("ユーザー名またはパスワードが間違っています"),
      ).toBeInTheDocument();
    });
  },
);
