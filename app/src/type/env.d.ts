declare global {
  namespace NodeJS {
    interface ProcessEnv {
      AUTH_SECRET: string;
      API_URL: string;
    }
  }
}

export {};
