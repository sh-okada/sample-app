import { expect } from "@playwright/test";
import { test } from "./fixtures";

test("ユーザー名が1文字以下の場合、エラーメッセージが表示されること", async ({
  page,
}) => {
  await page.goto("/signup");
  await page.getByTestId("username-input").fill("a");
  await page.getByTestId("username-input").blur();

  await expect(page.getByTestId("username-error-text")).toHaveText(
    "ユーザー名は2文字以上で入力してください",
  );
});

test("ユーザー名が9文字以上の場合、エラーメッセージが表示されること", async ({
  page,
}) => {
  await page.goto("/signup");
  await page.getByTestId("username-input").fill("abcdefghij");
  await page.getByTestId("username-input").blur();

  await expect(page.getByTestId("username-error-text")).toHaveText(
    "ユーザー名は8文字以下で入力してください",
  );
});

test("使用されていないユーザー名の場合、ユーザー登録できること", async ({
  page,
  mockServerRequest,
}) => {
  await mockServerRequest.POST("http://api:8000/api/auth/signup", {
    status: 201,
    body: {
      detail: "User created successfully.",
    },
  });

  await page.goto("/signup");
  await page.getByTestId("username-input").fill("sh-okada");
  await page.getByTestId("password-input").fill("Password123");
  await page.getByTestId("signup-button").click();

  await expect(page).toHaveURL("/login");
});

test("使用されているユーザー名の場合、エラーメッセージが表示されること", async ({
  page,
  mockServerRequest,
}) => {
  await mockServerRequest.POST("http://api:8000/api/auth/signup", {
    status: 400,
    body: {
      detail: "Username is already in use.",
    },
  });

  await page.goto("/signup");
  await page.getByTestId("username-input").fill("sh-okada");
  await page.getByTestId("password-input").fill("Password123");
  await page.getByTestId("signup-button").click();

  await expect(
    page.getByText("ユーザー名は既に使用されています。"),
  ).toBeVisible();
});
