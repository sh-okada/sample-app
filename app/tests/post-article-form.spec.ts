import { expect } from "@playwright/test";
import { test } from "./fixtures";

test("タイトルが未入力の場合、エラーメッセージが表示されること", async ({
  page,
  mockServerRequest,
}) => {
  await mockServerRequest.POST(
    {
      url: "http://api:8000/api/auth/login",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: "username=sh-okada&password=Password123",
    },
    {
      status: 200,
      body: {
        id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
        username: "sh-okada",
        access_token: "fake-access-token",
        refresh_token: "fake-refresh-token",
      },
    },
  );

  await page.goto("/article/post");
  await page.getByTestId("username-input").fill("sh-okada");
  await page.getByTestId("password-input").fill("Password123");
  await page.getByTestId("login-button").click();

  await page.getByTestId("post-article-button").click();

  await expect(page.getByTestId("article-title-error-text")).toHaveText(
    "タイトルは必須項目です",
  );
});
