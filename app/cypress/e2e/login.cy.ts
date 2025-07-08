describe("Navigation", () => {
  it("should navigate to the about page", () => {
    cy.visit("http://localhost:3000/login");

    // Find a link with an href attribute containing "about" and click it
    cy.get('[data-cy="username"]').type("user");
    cy.get('[data-cy="password"]').type("password");
  });
});
