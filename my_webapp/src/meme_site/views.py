from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import ListView, RedirectView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import MemePost, Comment_section
from .forms import CommentForm
from django.db.models import Q
# Create your views here.

class MemeListView(ListView):
    model = MemePost
    template_name = 'meme_site/meme_site.html'
    context_object_name = 'memes'
    ordering = ['-date_added']

    

    def get_queryset(self):
        _objects = MemePost.objects.filter().all()
        _new_objects = []
        for obj in _objects:
            if obj.thumb_up.count() >= 3:
                _new_objects.append(obj)
                
                
        return _new_objects


class MemeLobby(ListView):
    model = MemePost
    template_name = 'meme_site/meme_lobby.html'
    context_object_name = 'memes'


    def get_queryset(self):
        _objects = MemePost.objects.filter().all()
        _new_objects = []
        for obj in _objects:
            if obj.thumb_up.count() < 3:
                _new_objects.append(obj)

        return _new_objects



class UserMemeListView(ListView):
    model = MemePost
    template_name ='meme_site/user_memes.html'
    context_object_name = 'memes'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return MemePost.objects.filter(user=user).order_by('-date_added')


def memeDetailView(request, id):
    post = get_object_or_404(MemePost, id=id)
    comments = Comment_section.objects.filter(post=post).order_by('-id')
    template_name = 'meme_site/meme_detail.html'

    # creating field where we can write comment
    comment_form = CommentForm(request.POST or None)

    # if we write someting to this
    if comment_form.is_valid():
        # then take our content field from CommentForm
        content = request.POST.get('content')
        # then create comment were post will be actual post, user will be requested user
        # and content taken from comment_form
        comment = Comment_section.objects.create(post=post, user=request.user, content=content)
        # then save it and return actual site
        comment.save()
        return redirect(post.get_absolute_url())
    else:
        comment_form= CommentForm()
    
    ## To be refactored ..
    ## maybe just make here the function of thumbs_up and down
    thumbed_up = False 
    user = request.user
    if post.thumb_up.filter(id=user.id).exists():
        thumbed_up = True 

    thumbed_down = False 
    if post.thumb_down.filter(id=user.id).exists():
        thumbed_down = True 

    context = {
        'my_object': post,
        'my_comments': comments,
        'comment_form': comment_form,
        'thumbed_up': thumbed_up,
        'thumbed_down': thumbed_down,
    }

    return render(request, template_name, context)


class MemeAddView(LoginRequiredMixin, CreateView):
    model = MemePost
    fields = ['title', 'image']
    template_name = 'meme_site/meme_add.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required
def deleteMeme(request, id):
    my_meme = get_object_or_404(MemePost, id=id)
    
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


# working on class
class Meme_like_up(RedirectView):
    # function that will add us like up where we will get 3 argumnets
    def get_redirect_url(self, *args, **kwargs):
        # taking the ID of object - each of meme detail view
        id = self.kwargs.get("id")
        # taking the object from MemePost list with ID
        object_like = get_object_or_404(MemePost, id=id)
        # creating my return url
        url_ = object_like.get_absolute_url()
        # taking THIS user from request
        user = self.request.user
        # thumbed_up taking to False and if we thumbed_up then we will return to True
        thumbed_up = False 
        if object_like.thumb_up.filter(id=user.id).exists():
            object_like.thumb_up.remove(user)
            thumbed_up = False
        else:
            object_like.thumb_up.add(user)
            thumbed_up = True 
      
        ## Another method of thumb_up add and remove
        # # if user is logged in then add a point to thumb_up in object_like
        # if user.is_authenticated:
        #     if user in object_like.thumb_up.exists:
        #         object_like.thumb_up.remove(user)
        #         thumbed_up = False
        #     else:
        #         object_like.thumb_up.add(user)
        #         thumbed_up = True
        # return absolute url
        return url_

class Like_down(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        # taking specific object
        object_unlike = get_object_or_404(MemePost, id=self.kwargs.get("id"))
        # taking absolute return url
        url_ = object_unlike.get_absolute_url()
        # taking specific user
        user = self.request.user
        # thumbed_down taking to False and if we thumbed_down then we will return to True
        thumbed_down = False 
        if object_unlike.thumb_down.filter(id=user.id).exists():
            object_unlike.thumb_down.remove(user)
            thumbed_down = False 
        else:
            object_unlike.thumb_down.add(user)
            thumbed_down = True 

        ### Anoher method if already thumbed down or not
        # # if user is authenticated then:
        # if user.is_authenticated:
        #     # if user already unliked this meme then
        #     if user in object_unlike.thumb_down.all():
        #         # remove his unlike
        #         object_unlike.thumb_down.remove(user)
        #         thumbed_down = False 
        #     else:
        #         # if he didn't unlike then unlike it
        #         object_unlike.thumb_down.add(user)
        #         thumbed_down = True
        # return to specific meme
        return url_



    

    
