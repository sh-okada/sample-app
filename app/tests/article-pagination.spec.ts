import { expect } from "@playwright/test";
import { test } from "./fixtures";

test.beforeEach(async ({ mockServerRequest }) => {
  await mockServerRequest.GET(
    {
      url: "http://api:8000/api/articles",
      query: { page: 1, limit: 5, q: "" },
    },
    {
      body: {
        values: [
          {
            id: "51a679c2-2062-4e6c-93b3-af1c681bb281",
            title: "1",
            text: "# Hello World",
            published_at: "2025-07-23T00:00:00",
            user: {
              id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
              name: "sh-okada",
            },
          },
          {
            id: "69c042b2-85c8-418a-899a-dbcb62cad338",
            title: "2",
            text: "# Hello World",
            published_at: "2025-07-23T00:00:00",
            user: {
              id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
              name: "sh-okada",
            },
          },
          {
            id: "abd32f0d-2a34-4ece-bc79-fadb37a51353",
            title: "3",
            text: "# Hello World",
            published_at: "2025-07-23T00:00:00",
            user: {
              id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
              name: "sh-okada",
            },
          },
          {
            id: "4ae7a5a9-27da-4f36-a130-d6e9319cc052",
            title: "4",
            text: "# Hello World",
            published_at: "2025-07-23T00:00:00",
            user: {
              id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
              name: "sh-okada",
            },
          },
          {
            id: "8e217aff-19cd-46da-9104-64e26fef303f",
            title: "5",
            text: "# Hello World",
            published_at: "2025-07-23T00:00:00",
            user: {
              id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
              name: "sh-okada",
            },
          },
        ],
        count: 15,
        total_pages: 3,
      },
    },
  );

  await mockServerRequest.GET(
    {
      url: "http://api:8000/api/articles",
      query: { page: 2, limit: 5, q: "" },
    },
    {
      body: {
        values: [
          {
            id: "a4404bbe-c8b8-40c3-98d4-8f2754251464",
            title: "6",
            text: "# Hello World",
            published_at: "2025-07-23T23:00:00Z",
            user: {
              id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
              name: "sh-okada",
            },
          },
          {
            id: "a11fd7c1-6cee-4ec9-aba5-090cbbd37c22",
            title: "7",
            text: "# Hello World",
            published_at: "2025-07-23T00:00:00",
            user: {
              id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
              name: "sh-okada",
            },
          },
          {
            id: "44eee787-4081-4500-a04d-22c0b670c296",
            title: "8",
            text: "# Hello World",
            published_at: "2025-07-23T00:00:00",
            user: {
              id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
              name: "sh-okada",
            },
          },
          {
            id: "f48432e7-dc41-4f1f-b7b7-2038e9ebbb23",
            title: "9",
            text: "# Hello World",
            published_at: "2025-07-23T00:00:00",
            user: {
              id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
              name: "sh-okada",
            },
          },
          {
            id: "6a416cd6-a24c-4057-b483-08d2547f23a7",
            title: "10",
            text: "# Hello World",
            published_at: "2025-07-23T00:00:00",
            user: {
              id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
              name: "sh-okada",
            },
          },
        ],
        count: 15,
        total_pages: 3,
      },
    },
  );

  await mockServerRequest.GET(
    {
      url: "http://api:8000/api/articles",
      query: { page: 3, limit: 5, q: "" },
    },
    {
      body: {
        values: [
          {
            id: "1fd47c4f-c936-495b-85e1-c7e0b1618dcc",
            title: "11",
            text: "# Hello World",
            published_at: "2025-07-23T23:00:00Z",
            user: {
              id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
              name: "sh-okada",
            },
          },
          {
            id: "ae16789a-cd11-404b-982f-69a3e7617bed",
            title: "12",
            text: "# Hello World",
            published_at: "2025-07-23T00:00:00",
            user: {
              id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
              name: "sh-okada",
            },
          },
          {
            id: "bec88aa2-5690-407f-bc40-8e8d7da02883",
            title: "13",
            text: "# Hello World",
            published_at: "2025-07-23T00:00:00",
            user: {
              id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
              name: "sh-okada",
            },
          },
          {
            id: "8f040903-df95-4e53-8cde-d23c72785457",
            title: "14",
            text: "# Hello World",
            published_at: "2025-07-23T00:00:00",
            user: {
              id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
              name: "sh-okada",
            },
          },
          {
            id: "7c514b79-ac95-4368-a365-ed8043eb236c",
            title: "15",
            text: "# Hello World",
            published_at: "2025-07-23T00:00:00",
            user: {
              id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
              name: "sh-okada",
            },
          },
        ],
        count: 15,
        total_pages: 3,
      },
    },
  );
});

test.describe("1/3ページ目の場合", () => {
  test("現在のページが1/3で表示されていること", async ({ page }) => {
    await page.goto("/");

    await expect(page.getByTestId("current-page")).toHaveText("1/3");
  });

  test("次のページに遷移できること", async ({ page }) => {
    await page.goto("/");
    await page.getByTestId("next-page-button").click();

    await expect(page).toHaveURL("/?page=2");
  });

  test("最後のページに遷移できること", async ({ page }) => {
    await page.goto("/");
    await page.getByTestId("last-page-button").click();

    await expect(page).toHaveURL("/?page=3");
  });

  test("前のページに遷移できないこと", async ({ page }) => {
    await page.goto("/");
    await page.getByTestId("prev-page-button").click();

    await expect(page).toHaveURL("/");
  });

  test("最初のページに遷移できないこと", async ({ page }) => {
    await page.goto("/");
    await page.getByTestId("first-page-button").click();

    await expect(page).toHaveURL("/");
  });
});

test.describe("2/3ページ目の場合", () => {
  test("現在のページが2/3で表示されていること", async ({ page }) => {
    await page.goto("/?page=2");

    await expect(page.getByTestId("current-page")).toHaveText("2/3");
  });

  test("次のページに遷移できること", async ({ page }) => {
    await page.goto("/?page=2");
    await page.getByTestId("next-page-button").click();

    await expect(page).toHaveURL("/?page=3");
  });

  test("最後のページに遷移できること", async ({ page }) => {
    await page.goto("/?page=2");
    await page.getByTestId("last-page-button").click();

    await expect(page).toHaveURL("/?page=3");
  });

  test("前のページに遷移できること", async ({ page }) => {
    await page.goto("/?page=2");
    await page.getByTestId("prev-page-button").click();

    await expect(page).toHaveURL("/");
  });

  test("最初のページに遷移できること", async ({ page }) => {
    await page.goto("/?page=2");
    await page.getByTestId("first-page-button").click();

    await expect(page).toHaveURL("/");
  });
});

test.describe("3/3ページ目の場合", () => {
  test("現在のページが3/3で表示されていること", async ({ page }) => {
    await page.goto("/?page=3");

    await expect(page.getByTestId("current-page")).toHaveText("3/3");
  });

  test("次のページに遷移できないこと", async ({ page }) => {
    await page.goto("/?page=3");
    await page.getByTestId("next-page-button").click();

    await expect(page).toHaveURL("/?page=3");
  });

  test("最後のページに遷移できないこと", async ({ page }) => {
    await page.goto("/?page=3");
    await page.getByTestId("last-page-button").click();

    await expect(page).toHaveURL("/?page=3");
  });

  test("前のページに遷移できること", async ({ page }) => {
    await page.goto("/?page=3");
    await page.getByTestId("prev-page-button").click();

    await expect(page).toHaveURL("/?page=2");
  });

  test("最初のページに遷移できること", async ({ page }) => {
    await page.goto("/?page=3");
    await page.getByTestId("first-page-button").click();

    await expect(page).toHaveURL("/");
  });
});
