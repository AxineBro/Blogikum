from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from blog.models import Post
from django.core.paginator import Paginator

User = get_user_model()


class ProfileDetailView(DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_posts = Post.objects.filter(author=self.object)
        paginator = Paginator(user_posts, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        return context
