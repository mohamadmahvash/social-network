from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .models import Post
from django.contrib import messages


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, "home/index.html", {'posts': posts})


class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(id=post_id, slug=post_slug)
        return render(request, 'home/detail.html', {'post': post})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        if post.owner.id == request.user.id:
            post.delete()
            messages.success(request, 'Post deleted successfully', extra_tags='success')
        else:
            messages.error(request, 'You can not delete this post', extra_tags='danger')
        return redirect('home:home')
