import { render, screen } from "@testing-library/react";
import AxiosMockAdapter from "axios-mock-adapter";
import Page from "@/app/(with-header)/page";
import { axiosInstance } from "@/lib/axios";

/**
 * 記事の一覧
 *  各記事へのリンク先は「/article/{id}」が設定されていること
 */

describe("記事の一覧", () => {
  // let axiosMock = new AxiosMockAdapter(axiosInstance, { delayResponse: 2000 });
  let axiosMock: AxiosMockAdapter;

  beforeEach(() => {
    axiosMock = new AxiosMockAdapter(axiosInstance);
    axiosMock.onGet("/api/articles").reply(200, [
      {
        id: "29610f16-c35e-4dd8-b1d4-244cf9bfd08c",
        title: "タイトル1",
        text: "テキスト1",
        user: { id: "7c6d33ab-a001-48bb-a744-f3e834d64b21", name: "user1" },
      },
      {
        id: "a7b5361e-cda6-4a3d-af98-490fbfcbe858",
        title: "タイトル2",
        text: "テキスト2",
        user: { id: "a83bcdb3-7bca-4fcc-8cc8-9cca154f58ae", name: "user1" },
      },
    ]);
    render(<Page searchParams={Promise.resolve({})} />);
  });

  afterEach(() => {
    axiosMock.restore();
  });

  test("各記事へのリンク先は「/article/{id}」が設定されていること", () => {
    expect(screen.findByText("タイトル1")).toHaveAttribute(
      "href",
      "/article/29610f16-c35e-4dd8-b1d4-244cf9bfd08c",
    );
    expect(screen.findByText("タイトル2")).toHaveAttribute(
      "href",
      "/article/a7b5361e-cda6-4a3d-af98-490fbfcbe858",
    );
  });
});
