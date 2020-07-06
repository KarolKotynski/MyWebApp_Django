import datetime

from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, RedirectView, CreateView, DetailView
from django.views.generic.edit import FormMixin
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import MemePost, CommentSection
from .forms import CommentForm
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
        context['form'] = self.get_form()
        current_meme = get_object_or_404(MemePost, id=self.object.id)
        context['thumbed_up'] = current_meme.thumb_up.filter(id=self.request.user.id).exists()
        context['thumbed_down'] = current_meme.thumb_down.filter(id=self.request.user.id).exists()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

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

    



# def meme_detail_view(request, id):
#     """
#     Showing one particular meme where is able to like or unlike this meme
#     Logged users can add comments at the below of the meme
#     Comment form is created using forms.py (CommentForm)
#     """
#     post = get_object_or_404(MemePost, id=id)
#     comments = CommentSection.objects.filter(post=post).order_by('-id')
#     template_name = 'meme_site/meme_detail2.html'

#     # creating field where we can write comment
#     comment_form = CommentForm(request.POST or None)

#     # if we write someting to this
#     if comment_form.is_valid():
#         # then take our content field from CommentForm
#         content = request.POST.get('content')
#         # then create comment were post will be actual post, user will be requested user
#         # and content taken from comment_form
#         comment = CommentSection.objects.create(
#             post=post, user=request.user, content=content)
#         # then save it and return actual site
#         comment.save()
#         return redirect(post.get_absolute_url())
#     else:
#         comment_form = CommentForm()

#     current_date = datetime.datetime.now()

#     date_delay = comments

#     # To be refactored ..
#     # maybe just make here the function of thumbs_up and down
#     thumbed_up = False
#     user = request.user
#     if post.thumb_up.filter(id=user.id).exists():
#         thumbed_up = True

#     thumbed_down = False
#     if post.thumb_down.filter(id=user.id).exists():
#         thumbed_down = True

#     context = {
#         'my_object': post,
#         'my_comments': comments,
#         'comment_form': comment_form,
#         'thumbed_up': thumbed_up,
#         'thumbed_down': thumbed_down,
#         'current_date': current_date,
#     }
#     return render(request, template_name, context)


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


@login_required
def delete_meme(request, pk):
    """
    function to delete meme if requested user is author of this meme.
    """
    my_meme = get_object_or_404(MemePost, pk=pk)

    userRequest = request.user.id
    author = my_meme.user.id

    if request.method == 'POST':
        if userRequest == author:
            my_meme.delete()
            return redirect('memeListView')

    if request.method == 'GET':
        if userRequest != author:
            return redirect('memeListView')

    context = {
        'my_meme': my_meme,
        'userRequestes': userRequest
    }
    template = 'meme_site/meme_delete.html'

    return render(request, template, context)


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
