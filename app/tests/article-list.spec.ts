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
            title: "title1",
            text: "# Hello World",
            published_at: "2025-07-23T00:00:00",
            user: {
              id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
              name: "sh-okada",
            },
          },
          {
            id: "69c042b2-85c8-418a-899a-dbcb62cad338",
            title: "title2",
            text: "# Hello World",
            published_at: "2025-07-23T00:00:00",
            user: {
              id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
              name: "sh-okada",
            },
          },
          {
            id: "abd32f0d-2a34-4ece-bc79-fadb37a51353",
            title: "title3",
            text: "# Hello World",
            published_at: "2025-07-23T00:00:00",
            user: {
              id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
              name: "sh-okada",
            },
          },
          {
            id: "4ae7a5a9-27da-4f36-a130-d6e9319cc052",
            title: "title4",
            text: "# Hello World",
            published_at: "2025-07-23T00:00:00",
            user: {
              id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
              name: "sh-okada",
            },
          },
          {
            id: "8e217aff-19cd-46da-9104-64e26fef303f",
            title: "title5",
            text: "# Hello World",
            published_at: "2025-07-23T00:00:00",
            user: {
              id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
              name: "sh-okada",
            },
          },
        ],
        count: 10,
        total_pages: 2,
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
            title: "title6",
            text: "# Hello World",
            published_at: "2025-07-23T23:00:00Z",
            user: {
              id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
              name: "sh-okada",
            },
          },
          {
            id: "a11fd7c1-6cee-4ec9-aba5-090cbbd37c22",
            title: "title7",
            text: "# Hello World",
            published_at: "2025-07-23T00:00:00",
            user: {
              id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
              name: "sh-okada",
            },
          },
          {
            id: "44eee787-4081-4500-a04d-22c0b670c296",
            title: "title8",
            text: "# Hello World",
            published_at: "2025-07-23T00:00:00",
            user: {
              id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
              name: "sh-okada",
            },
          },
          {
            id: "f48432e7-dc41-4f1f-b7b7-2038e9ebbb23",
            title: "title9",
            text: "# Hello World",
            published_at: "2025-07-23T00:00:00",
            user: {
              id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
              name: "sh-okada",
            },
          },
          {
            id: "6a416cd6-a24c-4057-b483-08d2547f23a7",
            title: "title10",
            text: "# Hello World",
            published_at: "2025-07-23T00:00:00",
            user: {
              id: "c36feca1-ef32-46cc-9df4-3c0eeb698251",
              name: "sh-okada",
            },
          },
        ],
        count: 10,
        total_pages: 2,
      },
    },
  );
});

test("1ページ目の場合、1~5件目の記事が表示される", async ({ page }) => {
  await page.goto("/");
  const articleTitles = await page
    .getByTestId("article-title")
    .allTextContents();

  expect(articleTitles).toStrictEqual([
    "title1",
    "title2",
    "title3",
    "title4",
    "title5",
  ]);
});

test("2ページ目の場合、6~10件目の記事が表示される", async ({ page }) => {
  await page.goto("/?page=2");

  const articleTitles = await page
    .getByTestId("article-title")
    .allTextContents();

  expect(articleTitles).toStrictEqual([
    "title6",
    "title7",
    "title8",
    "title9",
    "title10",
  ]);
});
