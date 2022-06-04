from .core import PostsService, TagsService, CommentsService, UsersService

#: An instance of the :class:`UsersService` class
user_service = UsersService()

#: An instance of the :class:`PostsService` class
post_service = PostsService()

#: An instance of the :class:`TagsService` class
tag_service = TagsService()

#: An instance of the :class:`CommentsService` class
comment_service = CommentsService()
