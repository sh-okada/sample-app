import NextAuth from "next-auth";
import Credentials from "next-auth/providers/credentials";
import { login } from "@/api/auth";
import { paths } from "@/config/paths";
import { loginSchema } from "@/lib/zod/schema";

const publicRoutes = [
  paths.home.getHref(),
  paths.login.getHref(),
  paths.signup.getHref(),
];

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Credentials({
      credentials: {
        username: {},
        password: {},
      },
      authorize: async (credentials) => {
        const loginFormData = loginSchema.parse(credentials);

        const res = (await login(loginFormData)).data;

        return {
          id: res.userId,
          name: res.username,
          accessToken: res.accessToken,
        };
      },
    }),
  ],
  pages: {
    signIn: paths.login.getHref(),
  },
  callbacks: {
    redirect: async ({ url, baseUrl }) => {
      const parsedUrl = new URL(url);
      const callbackUrl = parsedUrl.searchParams.get("callbackUrl");

      if (callbackUrl) {
        return callbackUrl;
      }

      return baseUrl;
    },
    jwt: async ({ token, user }) => {
      if (user) {
        token.sub = user.id;
        token.name = user.name;
        token.accessToken = user.accessToken;
      }
      return token;
    },
    session: async ({ session, token }) => {
      if (token.sub) {
        session.user.id = token.sub;
        session.user.name = token.name;
        session.user.accessToken = token.accessToken;
      }

      return session;
    },
    authorized: async ({ auth, request: { nextUrl } }) => {
      if (!auth && publicRoutes.includes(nextUrl.pathname)) {
        return true;
      }

      return !!auth;
    },
  },
});
