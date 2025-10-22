import { expect } from "@playwright/test";
import { test } from "./fixtures";

test.beforeEach(async ({ mockServerRequest }) => {
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
});

test("callbackUrlクエリパラメータがある場合、callbackUrlにリダイレクトされること", async ({
  page,
}) => {
  await page.goto("/login?callbackUrl=/article/post");
  await page.getByTestId("username-input").fill("sh-okada");
  await page.getByTestId("password-input").fill("Password123");
  await page.getByTestId("login-button").click();
  await page.waitForURL("/article/post");

  expect(page.url()).toBe("http://localhost:3000/article/post");
});

test("callbackUrlクエリパラメータがない場合、トップページに遷移すること", async ({
  page,
}) => {
  await page.goto("/login");
  await page.getByTestId("username-input").fill("sh-okada");
  await page.getByTestId("password-input").fill("Password123");
  await page.getByTestId("login-button").click();
  await page.waitForURL("/");

  expect(page.url()).toBe("http://localhost:3000/");
});
