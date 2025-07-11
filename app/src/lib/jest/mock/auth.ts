const NextAuthMock = {
  auth: {
    jwt: {
      secret: process.env.AUTH_SECRET,
    },
  },
  signIn: jest.fn(),
  signOut: jest.fn(),
  handlers: {
    GET: jest.fn(),
    POST: jest.fn(),
  },
};

export const {
  auth,
  signIn,
  signOut,
  handlers: { GET, POST },
} = NextAuthMock;
