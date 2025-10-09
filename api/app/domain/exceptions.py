class DomainException(Exception):
    pass


class MyPostArticle(DomainException):
    pass


class ArticleAlreadyLiked(DomainException):
    pass
