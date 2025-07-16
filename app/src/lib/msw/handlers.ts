import { HttpResponse, http, type RequestHandler } from "msw";

const helloHandler = [
  http.post("http://localhost:8000/api/auth/login", () => {
    return HttpResponse.json(
      {
        id: "id",
        username: "sh-okada",
        access_token: "fake-token",
      },
      { status: 400 },
    );
  }),
  http.get("http://localhost:8000/api/articles", () => {
    return HttpResponse.json([
      {
        id: "id",
        title: "title",
        text: "text",
        user: {
          id: "id",
          name: "name",
        },
      },
    ]);
  }),
  http.get("http://localhost:8000/api/articles/count", () => {
    return HttpResponse.json({ count: 1 });
  }),
];

export const handlers: RequestHandler[] = [...helloHandler];
