export const paths = {
  home: {
    name: "記事一覧",
    getHref: (query?: { page?: string }) =>
      query ? `/?${new URLSearchParams(query).toString()}` : "/",
  },
  login: {
    name: "ログイン",
    getHref: () => "/login",
  },
  signup: {
    name: "新規登録",
    getHref: () => "/signup",
  },
  article: {
    id: {
      name: "記事を見る",
      getHref: (id: string) => `/article/${id}`,
    },
    post: {
      name: "記事を書く",
      getHref: () => "/article/post",
    },
  },
} as const;
