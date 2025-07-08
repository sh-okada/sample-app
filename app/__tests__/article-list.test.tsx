import { act, render, screen } from "@testing-library/react";
import { ArticleListContainer } from "@/app/(with-header)/_components/article-list-container";
import { describeWithAxiosMock } from "@/lib/jest/util";

describeWithAxiosMock("記事が1件以上ある場合", (getAxiosMock) => {
  beforeEach(async () => {
    const axiosMock = getAxiosMock();
    axiosMock.onGet("/articles?page=1").reply(200, [
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
    await act(async () => {
      render(await ArticleListContainer({ page: 1 }));
    });
  });

  test("各記事へのリンク先は「/article/{id}」が設定されていること", async () => {
    expect(await screen.findByText("タイトル1")).toHaveAttribute(
      "href",
      "/article/29610f16-c35e-4dd8-b1d4-244cf9bfd08c",
    );
    expect(await screen.findByText("タイトル2")).toHaveAttribute(
      "href",
      "/article/a7b5361e-cda6-4a3d-af98-490fbfcbe858",
    );
  });
});

describeWithAxiosMock("記事が1件もない場合", (getAxiosMock) => {
  beforeEach(async () => {
    const axiosMock = getAxiosMock();
    axiosMock.onGet("/articles?page=1").reply(200, []);
    await act(async () => {
      render(await ArticleListContainer({ page: 1 }));
    });
  });

  test("「記事は投稿されていません」と表示されること", async () => {
    expect(
      await screen.findByText("記事は投稿されていません"),
    ).toBeInTheDocument();
  });
});
