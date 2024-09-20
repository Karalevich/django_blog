from django.shortcuts import render, get_object_or_404
from datetime import date
from .models import Post


# Create your views here.

def get_date(post):
    return post['date']

def index(request):
    latest_post = Post.objects.all().order_by('-date')[:3]
    return render(request, 'index.html', {
        'posts': latest_post
    })


def posts(request):
    all_posts = Post.objects.all().order_by('-date')
    return render(request, 'posts.html', {
        'all_posts': all_posts
    })


def post_detail(request, slug):
    post_data = get_object_or_404(Post, slug=slug)
    return render(request, 'post-detail.html', {
        'post': post_data,
        'tags': post_data.tags.all()
    })
