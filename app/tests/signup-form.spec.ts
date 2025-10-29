import { expect } from "@playwright/test";
import { test } from "./fixtures";

test("ユーザー名が未入力の場合、エラーメッセージが表示されること", async ({
  page,
}) => {
  await page.goto("/signup");
  await page.getByTestId("username-input").fill("");
  await page.getByTestId("username-input").blur();

  await expect(page.getByTestId("username-error-text")).toHaveText(
    "ユーザー名は必須項目です",
  );
});

test("ユーザー名が1文字以下の場合、エラーメッセージが表示されること", async ({
  page,
}) => {
  await page.goto("/signup");
  await page.getByTestId("username-input").fill("a");
  await page.getByTestId("username-input").blur();

  await expect(page.getByTestId("username-error-text")).toHaveText(
    "ユーザー名は2文字以上で入力してください",
  );
});

test("ユーザー名が9文字以上の場合、エラーメッセージが表示されること", async ({
  page,
}) => {
  await page.goto("/signup");
  await page.getByTestId("username-input").fill("abcdefghij");
  await page.getByTestId("username-input").blur();

  await expect(page.getByTestId("username-error-text")).toHaveText(
    "ユーザー名は8文字以下で入力してください",
  );
});

test("ユーザー名に「._-」以外の記号が含まれている場合、エラーメッセージが表示されること", async ({
  page,
}) => {
  await page.goto("/signup");
  await page.getByTestId("username-input").fill("sh@okada");
  await page.getByTestId("username-input").blur();

  await expect(page.getByTestId("username-error-text")).toHaveText(
    "ユーザー名は半角英数字と記号（._-）で入力してください",
  );
});

test("パスワードが未入力の場合、エラーメッセージが表示されること", async ({
  page,
}) => {
  await page.goto("/signup");
  await page.getByTestId("password-input").fill("");
  await page.getByTestId("password-input").blur();

  await expect(page.getByTestId("password-error-text")).toHaveText(
    "パスワードは必須項目です",
  );
});

test("パスワードが101文字以上の場合、エラーメッセージが表示されること", async ({
  page,
}) => {
  await page.goto("/signup");
  await page
    .getByTestId("password-input")
    .fill(
      "Password123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123",
    );
  await page.getByTestId("password-input").blur();

  await expect(page.getByTestId("password-error-text")).toHaveText(
    "パスワードは100文字以下で入力してください",
  );
});

test("パスワードが英小文字のみの場合、エラーメッセージが表示されること", async ({
  page,
}) => {
  await page.goto("/signup");
  await page.getByTestId("password-input").fill("password");
  await page.getByTestId("password-input").blur();

  await expect(page.getByTestId("password-error-text")).toHaveText(
    "パスワードには半角英（大文字・小文字）数字が含まれている必要があります",
  );
});

test("パスワードが英大文字のみの場合、エラーメッセージが表示されること", async ({
  page,
}) => {
  await page.goto("/signup");
  await page.getByTestId("password-input").fill("PASSWORD");
  await page.getByTestId("password-input").blur();

  await expect(page.getByTestId("password-error-text")).toHaveText(
    "パスワードには半角英（大文字・小文字）数字が含まれている必要があります",
  );
});

test("パスワードが数字のみの場合、エラーメッセージが表示されること", async ({
  page,
}) => {
  await page.goto("/signup");
  await page.getByTestId("password-input").fill("123456");
  await page.getByTestId("password-input").blur();

  await expect(page.getByTestId("password-error-text")).toHaveText(
    "パスワードには半角英（大文字・小文字）数字が含まれている必要があります",
  );
});

test("パスワードが英小文字+英大文字のみの場合、エラーメッセージが表示されること", async ({
  page,
}) => {
  await page.goto("/signup");
  await page.getByTestId("password-input").fill("Password");
  await page.getByTestId("password-input").blur();

  await expect(page.getByTestId("password-error-text")).toHaveText(
    "パスワードには半角英（大文字・小文字）数字が含まれている必要があります",
  );
});

test("パスワードが英小文字+数字のみの場合、エラーメッセージが表示されること", async ({
  page,
}) => {
  await page.goto("/signup");
  await page.getByTestId("password-input").fill("password123");
  await page.getByTestId("password-input").blur();

  await expect(page.getByTestId("password-error-text")).toHaveText(
    "パスワードには半角英（大文字・小文字）数字が含まれている必要があります",
  );
});

test("パスワードが英大文字+数字のみの場合、エラーメッセージが表示されること", async ({
  page,
}) => {
  await page.goto("/signup");
  await page.getByTestId("password-input").fill("PASSWORD123");
  await page.getByTestId("password-input").blur();

  await expect(page.getByTestId("password-error-text")).toHaveText(
    "パスワードには半角英（大文字・小文字）数字が含まれている必要があります",
  );
});
