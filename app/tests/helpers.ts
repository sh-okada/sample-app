import type { Page } from "@playwright/test";

export const getCookie = async (page: Page, name: string) => {
  const cookies = await page.context().cookies();
  const foundCookie = cookies.find((c) => c.name === name);

  return foundCookie;
};

export const waitForAddCookie = async (
  page: Page,
  name: string,
  timeout = 5000,
  interval = 100,
) => {
  const start = Date.now();
  while (Date.now() - start < timeout) {
    const foundCookie = await getCookie(page, name);
    if (typeof foundCookie !== "undefined") {
      return true;
    }
    await new Promise((r) => setTimeout(r, interval));
  }
  throw new Error(`Cookie "${name}" was not added within ${timeout} ms`);
};

export const waitForDeleteCookie = async (
  page: Page,
  name: string,
  timeout = 5000,
  interval = 100,
) => {
  const start = Date.now();
  while (Date.now() - start < timeout) {
    const foundCookie = await getCookie(page, name);
    if (typeof foundCookie === "undefined") {
      return true;
    }
    await new Promise((r) => setTimeout(r, interval));
  }
  throw new Error(`Cookie "${name}" was not deleted within ${timeout} ms`);
};
