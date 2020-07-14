import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import (
    HttpResponseRedirect,
    get_object_or_404,
    redirect,
    render
)
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    RedirectView
)
from django.views.generic.edit import FormMixin

from .forms import CommentForm
from .models import CommentSection, MemePost
from .utils import LikeMeme

# Create your views here.


class MemeListView(LikeMeme, ListView):
    """
    generate List view of memes which have at least 3 likes
    Memes are paginated by 5
    Memes are sorted from newest to the oldest
    """
    model = MemePost
    template_name = 'meme_site/meme_site.html'
    context_object_name = 'memes'
    paginate_by = 5

    def get_queryset(self):
        _objects = MemePost.objects.filter().all()
        _new_objects = []
        for obj in _objects:
            if obj.thumb_up.count() >= 3:
                _new_objects.append(obj)
        return _new_objects

class MemeLobby(ListView):
    """
    Lobby memes - at the beginning there get all of the memes where likes are below 3
    Lobby memes are paginated by 5
    Memes are sorted from newest to the oldest
    if meme get 3 likes then this meme will be rendered on the Main site
    """
    model = MemePost
    template_name = 'meme_site/meme_lobby.html'
    context_object_name = 'memes'
    paginate_by = 5

    def get_queryset(self):
        _objects = MemePost.objects.filter().all()
        _new_objects = []
        for obj in _objects:
            if obj.thumb_up.count() < 3:
                _new_objects.append(obj)

        return _new_objects


class UserMemeListView(ListView):
    """
    Collect all of user memes and paginate page by 5
    user memes are sorted from the newest to the oldest
    """
    model = MemePost
    template_name = 'meme_site/user_memes.html'
    context_object_name = 'memes'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return MemePost.objects.filter(user=user).order_by('-date_added')


class MemeDetailView(LikeMeme, FormMixin, DetailView):
    """
    This class render selected Meme from Meme List
    additionally showing its comments and we are able to add comment if we are logged in
    """
    model = MemePost
    template_name = 'meme_site/meme_detail.html'
    context_object_name = 'user_meme'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('memeDetailView', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(MemeDetailView, self).get_context_data(**kwargs)
        context['comments'] = CommentSection.objects.filter(post=self.kwargs.get('pk'))
        return context

    def form_valid(self, form, user):
        form.instance.post = self.object
        form.instance.user = user
        form.save()
        return super().form_valid(form)


class MemeAddView(LoginRequiredMixin, CreateView):
    """
    Class to create meme - we can only add title of meme and its image.
    if form is valid then meme will be created.
    """
    model = MemePost
    fields = ['title', 'image']
    template_name = 'meme_site/meme_add.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class MemeDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Class to delete meme and its associated comments
    """
    model = MemePost
    template_name = 'meme_site/meme_delete.html'

    def get_success_url(self):
        curren_meme = self.get_object().title
        messages.success(self.request, f"{curren_meme} deleted!")
        return reverse('memeListView')

    def test_func(self):
        my_meme = self.get_object()
        if self.request.user == my_meme.user:
            return True
        else:
            return False
