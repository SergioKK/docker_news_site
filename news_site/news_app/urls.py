from django.urls import path

from news_app.views import PostView, PostChange, vote_up, CommentView, CommentChange, view_post

urlpatterns = [
    path("posts/", PostView.as_view(), name="posts_view"),
    path("post/view/<int:pk>/", view_post, name="post_view"),
    path("post/change/<int:pk>/", PostChange.as_view(), name="post_change"),
    path("post/vote_up/<int:pk>/", vote_up, name="post_vote_up"),
    path("post/comments/", CommentView.as_view(), name="comments_view"),
    path("post/comment/<int:pk>/", CommentChange.as_view(), name="comment_change"),
]
