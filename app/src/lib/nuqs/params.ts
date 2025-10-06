import {
  createSearchParamsCache,
  createSerializer,
  parseAsInteger,
  parseAsString,
} from "nuqs/server";

export const searchArticleParams = {
  page: parseAsInteger.withDefault(1),
  q: parseAsString.withDefault(""),
};

export const searchArticleParamsCache =
  createSearchParamsCache(searchArticleParams);
export const serializeArticlesParams = createSerializer(searchArticleParams);
