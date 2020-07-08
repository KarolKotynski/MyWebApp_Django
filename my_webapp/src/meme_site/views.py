import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView, 
    ListView, 
    RedirectView,
    DeleteView
)
from django.views.generic.edit import FormMixin

from .forms import CommentForm
from .models import CommentSection, MemePost
from .utils import Thumb

# Create your views here.


class MemeListView(ListView):
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

    """
    We could merge CommentSection Model to MemeListView and we could use it.
    we could create class MemeDetailView(DetailView) and use it to show all comments of this meme
    we can call costam to see objects of CommentSection.
    costam.first.content show us the content of first comment.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['costam'] = CommentSection.objects.all()
        print(context)
        return context
    """


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


class MemeDetailView(FormMixin, DetailView):
    model = MemePost
    template_name = 'meme_site/meme_detail.html'
    context_object_name = 'user_meme'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('memeDetailView', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(MemeDetailView, self).get_context_data(**kwargs)
        context['comments'] = CommentSection.objects.filter(post=self.kwargs.get('pk'))
        current_meme = get_object_or_404(MemePost, id=self.object.id)
        context['thumbed_up'] = current_meme.thumb_up.filter(id=self.request.user.id).exists()
        context['thumbed_down'] = current_meme.thumb_down.filter(id=self.request.user.id).exists()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(form_class=CommentForm)
        print(form)

        if form.is_valid():
            user = self.request.user
            return self.form_valid(form, user)
        else:
            return self.form_invalid(form)

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
        return reverse('memeListView')

    def test_func(self):
        my_meme = self.get_object()
        if self.request.user == my_meme.user:
            return True
        else:
            return False


class MemeLikeUp(Thumb, RedirectView):
    """
    Class where we can add our like on the particular meme.
    if we liked this meme then we unable to dislike meme.
    Like works only one time at the requested user.
    """
    # function that will add us like up where we will get 3 argumnets
    thumbed = 'thumbed_up'
    model = MemePost
    


class MemeLikeDown(Thumb, RedirectView):
    """
    Class where we can add our unlike on the particular meme.
    if we unliked this meme then we unable to disunlike meme.
    Unlike works only one time at the requested user.
    """

    thumbed = 'thumbed_down'
    model = MemePost
