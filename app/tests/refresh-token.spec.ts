import { expect } from "@playwright/test";
import { test } from "./fixtures";
import { getCookie } from "./helpers";

test.describe("アクセストークンの有効期限が切れた場合", () => {
  test.beforeEach(async ({ page, mockServerRequest }) => {
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
    await mockServerRequest.POST(
      {
        url: "http://api:8000/api/articles",
        headers: {
          Authorization: "Bearer fake-access-token",
        },
        body: {
          title: "title1",
          text: "",
        },
      },
      { status: 401, body: { detail: "Token has expired." } },
    );
    await mockServerRequest.POST(
      {
        url: "http://api:8000/api/articles",
        headers: {
          Authorization: "Bearer new-fake-access-token",
        },
        body: {
          title: "title1",
          text: "",
        },
      },
      { status: 201, body: { detail: "Article created successfully." } },
    );
    await mockServerRequest.POST(
      {
        url: "http://api:8000/api/auth/tokens/refresh",
        body: {
          refresh_token: "fake-refresh-token",
        },
      },
      {
        status: 200,
        body: {
          access_token: "new-fake-access-token",
          refresh_token: "new-fake-refresh-token",
        },
      },
    );
    await mockServerRequest.GET(
      {
        url: "http://api:8000/api/articles",
        query: { page: 1, limit: 5, q: "" },
      },
      {
        body: {
          values: [
            {
              id: "1fd47c4f-c936-495b-85e1-c7e0b1618dcc",
              title: "title1",
              text: "",
              published_at: "2025-07-23T23:00:00Z",
              user: {
                id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
                name: "sh-okada",
              },
            },
          ],
          count: 1,
          total_pages: 1,
        },
      },
    );

    await page.goto("/article/post");
    await page.getByTestId("username-input").fill("sh-okada");
    await page.getByTestId("password-input").fill("Password123");
    await page.getByTestId("login-button").click();

    await page.getByTestId("article-title-input").fill("title1");
    await page.getByTestId("post-article-button").click();

    await expect(page).toHaveURL("/");
  });

  test("新しいアクセストークンがCookieに保存されること", async ({ page }) => {
    const accessToken = await getCookie(page, "access_token");

    expect(accessToken).toBeDefined();
    expect(accessToken?.value).toBe("new-fake-access-token");
  });

  test("新しいリフレッシュトークンがCookieに保存されること", async ({
    page,
  }) => {
    const refreshToken = await getCookie(page, "refresh_token");

    expect(refreshToken).toBeDefined();
    expect(refreshToken?.value).toBe("new-fake-refresh-token");
  });
});
