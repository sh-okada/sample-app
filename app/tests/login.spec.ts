import { expect, type Page } from "@playwright/test";
import { test } from "./fixtures";

const getCookie = async (
  page: Page,
  name: string,
  timeout = 5000,
  interval = 100,
) => {
  const start = Date.now();
  while (Date.now() - start < timeout) {
    const cookies = await page.context().cookies();
    const foundCookie = cookies.find((c) => c.name === name);
    if (foundCookie) {
      return foundCookie;
    }
    await new Promise((r) => setTimeout(r, interval));
  }
  return undefined;
};

test.describe("ユーザー名とパスワードが正しい場合", () => {
  test.beforeEach(async ({ page, mockServerRequest }) => {
    await mockServerRequest.POST("http://api:8000/api/auth/login", {
      status: 200,
      body: {
        id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
        username: "sh-okada",
        access_token: "fake-access-token",
        refresh_token: "fake-refresh-token",
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
  });

  test("ログインできること", async ({ page }) => {
    await expect(page).toHaveURL("/");
  });

  test("アクセストークンがCookieに保存されること", async ({ page }) => {
    const accessToken = await getCookie(page, "access_token");

    expect(accessToken).toBeDefined();
  });

  test("リフレッシュトークンがCookieに保存されること", async ({ page }) => {
    const refreshToken = await getCookie(page, "refresh_token");

    expect(refreshToken).toBeDefined();
  });

  test("セッショントークンがCookieに保存されること", async ({ page }) => {
    const sessionToken = await getCookie(page, "authjs.session-token");

    expect(sessionToken).toBeDefined();
  });
});

test("ユーザー名またはパスワードが間違っている場合、エラーメッセージが表示されること", async ({
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
});
