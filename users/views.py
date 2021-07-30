from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile

def loginUser(request):

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, "Username doesnot exists")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Username OR password is incorrect')


    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.error(request, 'Logged out Successfully')
    return redirect('login')


def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles':profiles}
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profileObj = Profile.objects.get(id=pk)
    
    topSkills = profileObj.skill_set.exclude(description__exact="")
    otherSkills = profileObj.skill_set.filter(description="")

    context = {
        'profile':profileObj,
        'topSkills':topSkills,
        'otherSkills':otherSkills
    }
    return render(request, 'users/user-profile.html', context)
