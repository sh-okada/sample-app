import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  reporter: [["html", { host: "0.0.0.0", port: "9323" }]],
  quiet: true,
  workers: 1,
  use: {
    baseURL: "http://localhost:3000",
    video: "on",
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],

  webServer: {
    command: "npm run dev:playwright",
    url: "http://localhost:3000/login",
  },
});
