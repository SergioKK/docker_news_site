from background_task.models import Task
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from news_app.models import Post, Comment, Vote
from news_app.serializer import PostSerializer, CommentSerializer
from news_app.tasks import delete_upvotes


class PostView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostChange(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentChange(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


@api_view(["GET"])
def vote_up(request, pk):
    like = get_object_or_404(Post.objects.all(), pk=pk)
    # checking if task not already exist
    if not Vote.objects.filter(post_id=like.pk).exists():
        delete_upvotes(
            like.pk, verbose_name="my_task_name", schedule=43200, repeat=Task.DAILY
        )
    try:
        like.upvote(request.user)
    except:
        return Response("Already voted")
    serializer = PostSerializer(like)
    return Response(serializer.data)


@api_view(["GET"])
def view_post(request, pk):
    like = get_object_or_404(Post.objects.all(), pk=pk)
    return redirect(like.link)
