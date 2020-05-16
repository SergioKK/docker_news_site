from background_task import background
from news_app.models import Vote, Post


@background(schedule=20)
def delete_upvotes(pk):
    # delete vote from post
    Vote.objects.filter(post_id=pk).delete()
    # set Post.votes equal to 0
    Post.objects.filter(id=pk).update(votes=0)
