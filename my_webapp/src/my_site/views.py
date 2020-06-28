from django.shortcuts import render, redirect, get_object_or_404
from .models import About_me, MySiteProfile
from .forms import UserRegisterForm, ProfileUpdateImgForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from meme_site.models import MemePost


# Create your views here.
posts = [
    {
    'title': 'hello world!'
    },
    {
    'title': 'hello world!'
    },
    {
    'title': 'hello world!'
    },
]

def home_page(request):

    context = {
        'posts': posts
        }
    return render(request, 'my_site/home_page.html', context)

def about_me(request):
    context = {
        'about': About_me.objects.filter(id=1).first()
    }
    
    return render(request, 'my_site/about_me.html', context)

# function to create an account
def register(request):
    # if we request to create an account
    if request.method == 'POST':
        # then we will use our form to create an account
        form = UserRegisterForm(request.POST)
        # if we our data are vaild then
        if form.is_valid():
            # save this form
            form.save()
            # get username from this form and
            username = form.cleaned_data.get("username")
            # print "<username> account crated!"
            messages.success(request, f"{username} account created!")
            # and redirect to register page - name taken from urls
            return redirect('mySiteLogin_page')
    else:
        # else clear page
        form=UserRegisterForm()
    # template of our register page
    template = 'my_site/register.html'
    # render template and take context from our form
    return render(request, template, {'form': form})


def profile(request, user):
    user_profile = get_object_or_404(MySiteProfile, user=User.objects.filter(username=user).first())
    user_requested = request.user
    print(user_profile.user.username)
    user_memes = MemePost.objects.filter(user=user_profile.user.id).order_by('-date_added')
    print(user_memes)
    

    

    if user_profile.user.username == user_requested.username:
        if request.method == "POST":
            user_profileform = ProfileUpdateImgForm(request.POST, request.FILES, instance=request.user.mysiteprofile)
            if user_profileform.is_valid():
                user_profileform.save()
                messages.success(request, f"{request.user}, your image has been changed")
                return redirect('mySiteProfile_page')
        else:
            user_profileform = ProfileUpdateImgForm(instance=request.user)
        context = {
            'profileform': user_profileform,
            'memes': user_memes,
        }
    else:
        context = {
        'user': user_profile.user,
        'user_requested': user_requested,
        'image': user_profile.image.url,
        'memes': user_memes,
        }

    template = 'my_site/profile.html'

    
  


    return render(request, template, context)