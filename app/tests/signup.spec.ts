import { expect } from "@playwright/test";
import { test } from "./fixtures";

test("使用されていないユーザー名の場合、ユーザー登録できること", async ({
  page,
  mockServerRequest,
}) => {
  await mockServerRequest.POST(
    {
      url: "http://api:8000/api/auth/signup",
      body: {
        username: "sh-okada",
        password: "Password123",
      },
    },
    {
      status: 201,
      body: {
        detail: "User created successfully.",
      },
    },
  );

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
  await mockServerRequest.POST(
    {
      url: "http://api:8000/api/auth/signup",
      body: {
        username: "sh-okada",
        password: "Password123",
      },
    },
    {
      status: 400,
      body: {
        detail: "Username is already in use.",
      },
    },
  );

  await page.goto("/signup");
  await page.getByTestId("username-input").fill("sh-okada");
  await page.getByTestId("password-input").fill("Password123");
  await page.getByTestId("signup-button").click();

  await expect(
    page.getByText("ユーザー名は既に使用されています。"),
  ).toBeVisible();
});
