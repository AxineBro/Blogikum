from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from .models import Post, Category
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.views.generic import UpdateView
from .forms import ProfileEditForm
from django.core.paginator import Paginator

User = get_user_model()


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
    ).order_by('-pub_date')

    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
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

    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj
    }

    return render(request, 'blog/category.html', context)


class ProfileUpdateView(UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog:user')

    def get_object(self):
        return self.request.user
