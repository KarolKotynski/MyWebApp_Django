from django.shortcuts import get_object_or_404
from .models import MemePost

class Thumb:
    thumbed = None
    model = None
    
    def get_redirect_url(self, pk, *args, **kwargs):
        # taking the ID of object - each of meme detail view
        pk = self.kwargs.get("pk")
        # taking the object from MemePost list with ID
        current_object = get_object_or_404(self.model, pk=pk)
        # creating my return url
        url_ = current_object.get_absolute_url()
        # taking THIS user from request
        user = self.request.user
        # thumbed taking to False and if we thumbed then we will return to True
        thumbed = self.thumbed

        if thumbed == 'thumbed_up':
            if current_object.thumb_up.filter(id=user.id).exists():
                current_object.thumb_up.remove(user)
                thumbed_up = False
            else:
                current_object.thumb_up.add(user)
                thumbed_up = True
        else:
            if current_object.thumb_down.filter(id=user.id).exists():
                current_object.thumb_down.remove(user)
                thumbed_down = False
            else:
                current_object.thumb_down.add(user)
                thumbed_down = True

        return url_
