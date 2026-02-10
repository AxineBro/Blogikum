from django.shortcuts import get_object_or_404, render
from .models import Post, Category
from django.utils import timezone


def get_published_posts():
    return Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )


def index(request):
    template = 'blog/index.html'

    posts = get_published_posts().select_related(
        'author',
        'location',
        'category'
    ).order_by('-pub_date')[:5]

    context = {
        'post_list': posts
    }
    return render(request, template, context)


def post_detail(request, post_id):

    post = get_object_or_404(
        get_published_posts().select_related('author', 'location', 'category'),
        pk=post_id
    )

    context = {
        'post': post
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    posts = category.posts.filter(
        is_published=True,
        pub_date__lte=timezone.now()
    ).select_related('author', 'location')

    context = {
        'category': category,
        'post_list': posts
    }

    return render(request, 'blog/category.html', context)
