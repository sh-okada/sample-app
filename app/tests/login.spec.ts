import { expect } from "@playwright/test";
import { test } from "./fixtures";

test("ユーザー名とパスワードが正しい場合、ログインできる", async ({
  page,
  mockServerRequest,
}) => {
  await mockServerRequest.POST("http://api:8000/api/auth/login", {
    status: 200,
    body: {
      id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
      username: "sh-okada",
      access_token: "fake-access-token",
    },
  });
  await mockServerRequest.GET("http://api:8000/api/articles", {
    status: 200,
    body: {
      values: [],
      count: 0,
      total_pages: 0,
    },
  });

  await page.goto("/login");
  await page.getByTestId("username-input").fill("sh-okada");
  await page.getByTestId("password-input").fill("Password123");
  await page.getByTestId("login-button").click();
  await page.waitForURL("/");

  expect(page.url()).toBe("http://localhost:3000/");
});

test("ユーザー名またはパスワードが間違っている場合、エラーメッセージが表示される", async ({
  page,
  mockServerRequest,
}) => {
  await mockServerRequest.POST("http://api:8000/api/auth/login", {
    status: 400,
    body: {
      detail: "Incorrect username or password.",
    },
  });

  await page.goto("/login");
  await page.getByTestId("username-input").fill("sh-okada");
  await page.getByTestId("password-input").fill("Password123");
  await page.getByTestId("login-button").click();

  await expect(
    page.getByText("ユーザ名またはパスワードが間違っています。"),
  ).toBeVisible();
});
