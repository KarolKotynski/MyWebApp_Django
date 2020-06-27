from django.contrib import admin
from .models import MemePost
from .forms import Comment_section
# Register your models here.

admin.site.register(MemePost)
admin.site.register(Comment_section)