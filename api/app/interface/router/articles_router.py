from typing import List

from fastapi import APIRouter, Response, status

from app.application import commands
from app.application.use_case.post_article_use_case import PostArticleUseCaseDep
from app.infrastructure.query_service.article_query_service import (
    ArticleQueryServiceDep,
)
from app.interface import requests, responses
from app.shared.oauth2 import CurrentUserDep

articles_router = APIRouter(prefix="/articles", tags=["articles"])


@articles_router.get("/count", response_model=responses.Article)
def get_article_count(article_query_service: ArticleQueryServiceDep):
    return article_query_service.get_article_count()


@articles_router.get("", response_model=List[responses.Article])
def get_docs(
    article_filter_query: requests.ArticleFilterQuery,
    article_query_service: ArticleQueryServiceDep,
):
    return article_query_service.get_articles(article_filter_query)


@articles_router.get("/{id}", response_model=responses.Article)
def get_doc(id: str, article_query_service: ArticleQueryServiceDep):
    article_id_path_param = requests.ArticleIdPathParam(id=id)

    return article_query_service.get_article(
        commands.GetArticle(article_id_path_param.id)
    )


@articles_router.post("")
def post_article(
    post_article_request: requests.PostArticle,
    post_article_use_case: PostArticleUseCaseDep,
    current_user: CurrentUserDep,
):
    post_article_use_case.execute(
        commands.PostArticle(
            post_article_request.title, post_article_request.text, current_user.id
        )
    )

    return Response(status_code=status.HTTP_201_CREATED)
