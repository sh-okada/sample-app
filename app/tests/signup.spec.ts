import { expect } from "@playwright/test";
import { test } from "./fixtures";

test("使用されていないユーザー名の場合、登録できる", async ({
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
  await page.waitForURL("/login");

  expect(page.url()).toBe("http://localhost:3000/login");
});

test("使用されているユーザー名の場合、エラーメッセージが表示される", async ({
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
