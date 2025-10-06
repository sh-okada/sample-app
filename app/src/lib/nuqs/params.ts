import {
  createSearchParamsCache,
  createSerializer,
  parseAsInteger,
} from "nuqs/server";

export const searchArticlesParams = {
  page: parseAsInteger.withDefault(1),
};

export const searchParamsCache = createSearchParamsCache(searchArticlesParams);
export const serializeArticlesParams = createSerializer(searchArticlesParams);
