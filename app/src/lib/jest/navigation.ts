export const { useRouter, usePathname, useSearchParams, useParams, redirect } =
  {
    useRouter: jest.fn(() => ({
      push: jest.fn(),
      replace: jest.fn(),
      prefetch: jest.fn(),
    })),
    usePathname: jest.fn(() => "/mock-path"),
    useSearchParams: jest.fn(() => ({
      get: jest.fn(),
    })),
    useParams: jest.fn(() => ({})),
    redirect: jest.fn(),
  };
