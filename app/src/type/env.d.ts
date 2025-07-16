declare global {
  namespace NodeJS {
    interface ProcessEnv {
      AUTH_SECRET: string;
      API_URL: string;
      NEXT_PUBLIC_MSW_MOCK: "enabled" | "disabled";
    }
  }
}

export {};
