import AxiosMockAdapter from "axios-mock-adapter";
import { AuthError } from "next-auth";
import { axiosInstance } from "@/lib/axios";

export const describeWithAxiosMock = (
  description: string,
  specDefinitions: (getAxiosMock: () => AxiosMockAdapter) => void,
) => {
  describe(description, () => {
    let axiosMock: AxiosMockAdapter;

    beforeEach(() => {
      axiosMock = new AxiosMockAdapter(axiosInstance);
    });

    afterEach(() => {
      axiosMock.restore();
    });

    specDefinitions(() => axiosMock);
  });
};

export const throwAuthError = (mockFn: jest.Mock, cause: Error) => {
  mockFn.mockImplementation(() => {
    throw new AuthError(cause);
  });
};
