from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.slug} - created at:{self.created}'

    def get_absolute_url(self):
        return reverse('home:post_detail', args=(self.id, self.slug))

    def like_count(self):
        return self.PostLikes.count()

    def user_can_like(self, user):
        user_likes = user.UserLikes.filter(post=self)
        if user_likes.exists():
            return True
        return False


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserComments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='PostComments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='ReplyComments'
                              , blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} : {self.body[:30]}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserLikes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='PostLikes')

    def __str__(self):
        return f'{self.user} : {self.post.slug}'
