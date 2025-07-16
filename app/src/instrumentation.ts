export const register = async () => {
  if (
    process.env.NEXT_RUNTIME === "nodejs" &&
    process.env.NEXT_PUBLIC_MSW_MOCK === "enabled"
  ) {
    const { server } = await import("@/lib/msw/server");
    server.listen({ onUnhandledRequest: "bypass" });
  }
};
