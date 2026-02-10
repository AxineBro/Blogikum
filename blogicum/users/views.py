from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from blog.models import Post

User = get_user_model()


class ProfileDetailView(DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_obj'] = Post.objects.filter(author=self.object)
        return context
