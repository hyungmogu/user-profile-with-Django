from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordChangeForm)
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('home')  # TODO: go to profile
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return HttpResponseRedirect(reverse('home'))  # TODO: go to profile
    return render(request, 'accounts/sign_up.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


@login_required
def password_edit(request):
    form = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        # check if user is currently logged in before proceeding
        if not request.user.is_active:
            messages.error(
                request,
                "User must be logged in to change password"
            )

            return HttpResponseRedirect(reverse('home'))

        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()

            # re-auth user to circumvent force log-out issue
            user = authenticate(
                username=request.user,
                password=form.cleaned_data['new_password1']
            )

            login(request, user)

            messages.success(
                request,
                "Password change is successful!"
            )

            return HttpResponseRedirect(reverse('home'))

    return render(request, 'accounts/password_edit.html', {
        'form': form
    })
