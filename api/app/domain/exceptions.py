class DomainException(Exception):
    pass


class MyPostArticleError(DomainException):
    pass


class ArticleAlreadyLikedError(DomainException):
    pass
