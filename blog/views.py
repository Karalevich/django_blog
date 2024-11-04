from django.shortcuts import render, get_object_or_404
from datetime import date
from .models import Post
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import CommentForm


# Create your views here.

class StartingPageView(ListView):
    template_name = 'index.html'
    model = Post
    ordering = ['-date']
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data

class AllPostsView(ListView):
    template_name = 'posts.html'
    model = Post
    ordering = ['-date']
    context_object_name = 'all_posts'

class SinglePostView(View):
    template_name = 'post-detail.html'
    model = Post

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            'post': post,
            'tags': post.tags.all(),
            'comment_form': CommentForm(),
            'comments': post.comments.all().order_by("-id")
        }
        return render(request, 'post-detail.html', context)
    
    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post =  Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('post-detail-page', args=[slug]))
        
        context = {
            'post': post,
            'tags': post.tags.all(),
            'comment_form': comment_form,
            'comments': post.comments.all().order_by("-id")
        }
        return render(request, 'post-detail.html', context)


class ReadLaterView(View):
    def post(self, request):
        pass