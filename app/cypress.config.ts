import { defineConfig } from "cypress";

export default defineConfig({
  e2e: {
    // biome-ignore lint/correctness/noUnusedFunctionParameters: <explanation>
    setupNodeEvents(on, config) {},
  },
  component: {
    devServer: {
      framework: "next",
      bundler: "webpack",
    },
  },
});
