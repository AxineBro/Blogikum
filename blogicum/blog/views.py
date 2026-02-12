from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from .models import Post, Category
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, DetailView, CreateView
from .forms import ProfileEditForm, PostForm
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

    def get_success_url(self):
        return reverse('blog:profile', args=[self.object.username])

    def get_object(self):
        return self.request.user


class ProfileDetailView(DetailView):
    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_posts = Post.objects.filter(author=self.object)
        paginator = Paginator(user_posts, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse('blog:profile', args=[self.object.author.username])

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
