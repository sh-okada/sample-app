import { expect } from "@playwright/test";
import { test } from "./fixtures";

test("callbackUrlクエリパラメータがある場合、callbackUrlにリダイレクトされる", async ({
  page,
  mockServerRequest,
}) => {
  await mockServerRequest.POST("http://api:8000/api/auth/login", {
    body: {
      id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
      username: "sh-okada",
      access_token: "fake-access-token",
    },
  });
  await mockServerRequest.GET("http://api:8000/api/articles", {
    body: {
      values: [],
      count: 0,
      total_pages: 0,
    },
  });

  await page.goto("/login?callbackUrl=/article/post");
  await page.getByTestId("username-input").fill("sh-okada");
  await page.getByTestId("password-input").fill("password");
  await page.getByTestId("login-button").click();
  await page.waitForURL("/article/post");

  expect(page.url()).toBe("http://localhost:3000/article/post");
});

test("callbackUrlクエリパラメータがない場合、トップページに遷移する", async ({
  page,
  mockServerRequest,
}) => {
  await mockServerRequest.POST("http://api:8000/api/auth/login", {
    body: {
      id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
      username: "sh-okada",
      access_token: "fake-access-token",
    },
  });
  await mockServerRequest.GET("http://api:8000/api/articles", {
    body: {
      values: [],
      count: 0,
      total_pages: 0,
    },
  });

  await page.goto("/login");
  await page.getByTestId("username-input").fill("sh-okada");
  await page.getByTestId("password-input").fill("password");
  await page.getByTestId("login-button").click();
  await page.waitForURL("/");

  expect(page.url()).toBe("http://localhost:3000/");
});
