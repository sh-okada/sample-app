describe("Navigation", () => {
  it("should navigate to the about page", () => {
    cy.intercept("POST", "http://localhost:8000/api/auth/login", {
      statusCode: 200,
      body: { id: "id1", username: "user1", access_token: "fake-token" },
    });

    cy.intercept("/api/auth/session", {
      statusCode: 200,
      body: {
        user: { id: "id1", name: "user1", accessToken: "fake-token" },
        expires: new Date(Date.now() + 60 * 60 * 1000).toISOString(),
      },
    });

    cy.intercept("GET", "/api/auth/callback/credentials", {
      statusCode: 200,
      body: {
        id: "id1",
        name: "user1",
        accessToken: "fake-token",
      },
    });

    cy.visit("http://localhost:3000/login");

    cy.get('[data-cy="username-input"]').type("user1");
    cy.get('[data-cy="password-input"]').type("password");
    cy.get('[data-cy="login-button"]').click();

    cy.url().should("be.a", "http://localhost:3000");
  });
});
