import { expect, test } from "@playwright/test";

test("ほげ", async ({ page }) => {
  // server.use(
  //   // Describe the network of the server-side Next.js.
  //   http.get("http://localhost:8000/api/articles", () => {
  //     return Response.json({ name: "John Maverick" }, { status: 500 });
  //   }),
  //   http.get("http://localhost:8000/api/articles/count", () => {
  //     return Response.json({ count: 20 });
  //   }),
  // );

  await page.goto("http://localhost:3000");

  expect(page.getByText("記事を見る")).toBeVisible();
});
