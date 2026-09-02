from django.views.generic import ListView
from .models import Post


class LabUpdateListView(ListView):
    model = Post
    template_name = 'lab_update/post_list.html'
    context_object_name = 'posts'
