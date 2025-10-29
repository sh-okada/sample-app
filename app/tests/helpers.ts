import type { Page } from "@playwright/test";

export const getCookie = async (
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
