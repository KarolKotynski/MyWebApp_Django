from django.contrib import admin
from .models import MemePost
from .forms import CommentSection
# Register your models here.

admin.site.register(MemePost)
admin.site.register(CommentSection)