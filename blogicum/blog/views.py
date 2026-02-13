from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, DetailView, CreateView, ListView, DeleteView
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Post, Category, Comment
from .forms import ProfileEditForm, PostForm, CommentForm
from .utils import get_published_posts

User = get_user_model()


class IndexListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 10

    def get_queryset(self):
        return get_published_posts().select_related(
            'author', 'location', 'category'
        ).annotate(
            comment_count=Count('comments', distinct=True)
        ).order_by('-pub_date')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        return get_published_posts().select_related(
            'author', 'location', 'category'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['form'] = CommentForm()
        return context


class CategoryPostsDetailView(DetailView):
    model = Category
    template_name = 'blog/category.html'
    context_object_name = 'category'
    slug_field = 'slug'
    slug_url_kwarg = 'category_slug'

    def get_queryset(self):
        return Category.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object

        posts = category.posts.filter(
            is_published=True,
            pub_date__lte=timezone.now()
        ).select_related(
            'author', 'location'
        ).annotate(
            comment_count=Count('comments', distinct=True)
        ).order_by('-pub_date')

        paginator = Paginator(posts, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
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

        user_posts = Post.objects.filter(author=self.object).annotate(
            comment_count=Count('comments', distinct=True)
        ).order_by('-pub_date')
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


class PostAccessMixin(LoginRequiredMixin, UserPassesTestMixin):
    model = Post
    template_name = 'blog/create.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff

    def handle_no_permission(self):
        post = self.get_object()
        return redirect('blog:post_detail', post_id=post.pk)


class PostUpdateView(PostAccessMixin, UpdateView):
    form_class = PostForm

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.id])


class PostDeleteView(PostAccessMixin, DeleteView):
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse('blog:profile', args=[self.object.author])


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post = get_object_or_404(
            get_published_posts(),
            pk=self.kwargs['post_id']
        )
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.post.pk])


class CommentAccessMixin(LoginRequiredMixin, UserPassesTestMixin):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def handle_no_permission(self):
        comment = self.get_object()
        return redirect('blog:post_detail', post_id=comment.post.pk)

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.post.pk])


class CommentUpdateView(CommentAccessMixin, UpdateView):
    form_class = CommentForm


class CommentDeleteView(CommentAccessMixin, DeleteView):
    pass
