from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from psycopg2._psycopg import IntegrityError


class Post(models.Model):
    title = models.CharField(max_length=200)
    author_name = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.URLField(max_length=200)
    date_creation = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def upvote(self, author_name):
        try:
            self.post_votes.create(author_name=author_name, post=self, vote_type="up")
            self.votes += 1
            self.save()
        except IntegrityError:
            return "already_upvoted"
        return "ok"

    def reset_votes(self):
        return Post.objects.all().update(rego_update=Post().rego_update)


class Comment(models.Model):
    post = models.ForeignKey("Post", related_name="comment", on_delete=models.CASCADE)
    author_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    date_creation = models.DateTimeField(auto_now_add=True)


class Vote(models.Model):
    author_name = models.ForeignKey(
        User, related_name="user_votes", on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post, related_name="post_votes", on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=200)

    class Meta:
        unique_together = ("author_name", "post", "vote_type")
