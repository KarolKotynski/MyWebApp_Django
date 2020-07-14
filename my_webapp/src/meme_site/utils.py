from django.shortcuts import HttpResponseRedirect, get_object_or_404

from .forms import CommentForm
from .models import MemePost

class LikeMeme:
    """
    This class has function post which like or unlike meme or 
    if we choose comment submit button our comment will be created.
    If we liked post we are able to return like and give unlike if we want to
    Is not possible to give like and unlike in one time.
    As a return we will be redirected to the same page where we were
    """
    def post(self, request, *args, **kwargs):
        # liked and unliked are a name of clicked button
        if 'liked' in request.POST or 'unliked' in request.POST:
            if request.method == "POST":
                user = request.user
                post_id = request.POST.get('meme_id')
                post_obj = MemePost.objects.get(pk = post_id)

                if 'liked' in request.POST:  
                    if user not in post_obj.thumb_up.all() and user not in post_obj.thumb_down.all():
                        post_obj.thumb_up.add(user)
                    elif user in post_obj.thumb_up.all() and user not in post_obj.thumb_down.all():
                        post_obj.thumb_up.remove(user)
                    else:
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

                if 'unliked' in request.POST:
                    if user not in post_obj.thumb_up.all() and user not in post_obj.thumb_down.all():
                        post_obj.thumb_down.add(user)
                    elif user not in post_obj.thumb_up.all() and user in post_obj.thumb_down.all():
                        post_obj.thumb_down.remove(user)
                    else:
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))       
        else:
            self.object = self.get_object()
            form = self.get_form(form_class=CommentForm)
            print(form)

            if form.is_valid():
                user = self.request.user
                return self.form_valid(form, user)
            else:
                return self.form_invalid(form)
