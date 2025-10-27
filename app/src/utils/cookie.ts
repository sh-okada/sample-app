import dayjs from "dayjs";
import { cookies } from "next/headers";

const setCookie = async (name: string, value: string, expires: Date) => {
  const cookieStore = await cookies();
  cookieStore.set({
    name: name,
    value: value,
    path: "/",
    expires: expires,
    httpOnly: true,
    sameSite: "lax",
  });
};

const getCookie = async (name: string) => {
  const cookieStore = await cookies();
  return cookieStore.get(name)?.value;
};

const deleteCookie = async (name: string) => {
  const cookieStore = await cookies();
  cookieStore.delete(name);
};

export const setAccessToken = async (accessToken: string) => {
  await setCookie(
    "access_token",
    accessToken,
    dayjs().add(1, "hours").toDate(),
  );
};

export const setRefreshToken = async (refreshToken: string) => {
  await setCookie(
    "refresh_token",
    refreshToken,
    dayjs().add(3, "months").toDate(),
  );
};

export const getAccessToken = async () => {
  return await getCookie("access_token");
};

export const getRefreshToken = async () => {
  return await getCookie("refresh_token");
};

export const deleteAccessToken = async () => {
  await deleteCookie("access_token");
};

export const deleteRefreshToken = async () => {
  await deleteCookie("refresh_token");
};
