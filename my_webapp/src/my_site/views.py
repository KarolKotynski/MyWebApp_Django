from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from .forms import UserRegisterForm, ProfileUpdateImgForm
from .models import AboutMe, MySiteProfile
from meme_site.models import MemePost



# Create your views here.

def register(request):
    """
    function to create an account
    We are using form from forms.py (UserRegisterForm)
    we have to input 4 variables: username, email, password and confirm password.
    if username is unique and passwords are correct then account will be created
    and we will be redirected to the login page.
    if not then we will be redirected again to register site with old inputs

    """
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



@login_required
def profile(request, user):
    """
    Getting user profile and its Memes from MemeSite and paginate the site to 3 memes per page
    if logged user is equal to requested user then we will be able to change user image profile
    using form from form.py (ProfileUpdateImgForm)
    if not then we will be able only to see user memes.
    """
    # get user profile name
    user_profile = get_object_or_404(MySiteProfile, user=User.objects.filter(username=user).first())
    
    # get user memes
    user_memes = MemePost.objects.filter(user=user_profile.user.id).order_by('-date_added')

    # get requested user name
    user_requested = request.user

    # paginate profile page - 3 memes per site.
    paginator_pages = Paginator(user_memes, 3)
    page = request.GET.get('page')
    user_memes = paginator_pages.get_page(page)
    
    # if user profile is equal to requested user then we can make changes on the profile
    # using form ProfileUpdateImgForm
    if user_profile.user.username == user_requested.username:
        if request.method == "POST":
            user_profileform = ProfileUpdateImgForm(request.POST, request.FILES, instance=request.user.mysiteprofile)
            if user_profileform.is_valid():
                user_profileform.save()
                messages.success(request, f"{request.user}, your image has been changed")
                
                return redirect(f"/profile/{user_profile.user.username}")
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