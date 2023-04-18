from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .forms import CreateUserForm, UpdateUserForm

# Create your views here.


def register_account(request):
    if request.user.is_authenticated:
        return redirect('books:home')

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_auth:login')

    context = {
        'form': form,
    }

    return render(request, 'registration/register.html', context)


def login_account(request):
    if request.user.is_authenticated:
        return redirect('books:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('books:home')

    return render(request, 'registration/login.html')


def edit_account(request):
    user = get_object_or_404(User, username=request.user)
    userform = UpdateUserForm(request.POST or None, instance=user)

    if request.method == 'POST':
        if userform.is_valid():
            userform.save()
            return redirect('books:home')

    context = {
        'form': userform,
        'user': user,
    }

    return render(request, 'registration/edit_user.html', context)


def logout_account(request):
    logout(request)
    return redirect('user_auth:login')
