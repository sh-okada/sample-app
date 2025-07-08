import AxiosMockAdapter from "axios-mock-adapter";
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
