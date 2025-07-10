import { http } from "msw";

export const handlers = [
  http.get("http://localhost:8000/api/articles", () => {
    return Response.json(
      {
        id: "id",
        title: "title",
        text: "text",
        user: { id: "id", name: "name" },
      },
      { status: 500 },
    );
  }),
  http.get("http://localhost:8000/api/articles/count", () => {
    return Response.json({ count: 20 });
  }),
];
