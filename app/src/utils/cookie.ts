import dayjs from "dayjs";
import { cookies } from "next/headers";

export const setAccessToken = async (token: string) => {
  const cookieStore = await cookies();
  cookieStore.set({
    name: "access_token",
    value: token,
    path: "/",
    expires: dayjs().add(1, "hour").toDate(),
    httpOnly: true,
    sameSite: "lax",
  });
};

export const getAccessToken = async () => {
  const cookieStore = await cookies();
  return cookieStore.get("access_token")?.value;
};

export const deleteAccessToken = async () => {
  const cookieStore = await cookies();
  cookieStore.delete("access_token");
};
