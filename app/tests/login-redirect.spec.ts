import { expect } from "@playwright/test";
import { test } from "./fixtures";

test.beforeEach(async ({ mockServerRequest }) => {
  await mockServerRequest.POST(
    {
      url: "http://api:8000/api/auth/login",
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
  await mockServerRequest.GET(
    {
      url: "http://api:8000/api/articles",
      query: { page: 1, limit: 5, q: "" },
    },
    {
      status: 200,
      body: {
        values: [],
        count: 0,
        total_pages: 0,
      },
    },
  );
});

test("callbackUrlクエリパラメータがある場合、callbackUrlにリダイレクトされること", async ({
  page,
}) => {
  await page.goto("/article/post");
  await page.getByTestId("username-input").fill("sh-okada");
  await page.getByTestId("password-input").fill("Password123");
  await page.getByTestId("login-button").click();

  await expect(page.getByTestId("page-title")).toHaveText("記事を書く");
});

test("callbackUrlクエリパラメータがない場合、トップページに遷移すること", async ({
  page,
}) => {
  await page.goto("/login");
  await page.getByTestId("username-input").fill("sh-okada");
  await page.getByTestId("password-input").fill("Password123");
  await page.getByTestId("login-button").click();

  await expect(page.getByTestId("page-title")).toHaveText("記事を見る");
});
