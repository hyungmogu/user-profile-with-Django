from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from accounts import forms, models


def home(request):
    return render(request, 'home.html')


@login_required
def profile_view(request):
    """
    Renders profile page. User profile is created if it doesn't exist
    (due to newly creation of account)
    """

    try:
        profile = models.Profile.objects.get(user=request.user)
    except models.Profile.DoesNotExist:
        profile = models.Profile.objects.create(user=request.user)

    return render(request, 'profile.html', {
        'profile': profile
    })


@login_required
def profile_edit(request):
    """
    Renders profile edit page. User profile is pre-filled, or created anew with
    empty fields if it doesn't exist. Form is saved only if the following
    criteria are satisfied:
        - Date of Birth is one of three formats: YYYY-MM-DD, MM/DD/YYYY,
        or MM/DD/YY.
        - Email and confirm email match and are in a valid format.
        - Short Bi have 10 characters or longer and properly escapes HTML
        formatting.
    """

    try:
        profile = models.Profile.objects.get(user=request.user)
        form = forms.ProfileForm(instance=profile)
    except models.Profile.DoesNotExist:
        form = forms.ProfileForm()
        profile = models.Profile.objects.create(user=request.user)

    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Profile information has been updated successfully"
            )

            return HttpResponseRedirect(reverse('profile_view'))

    return render(request, 'profile_edit.html', {
        'form': form
    })


@login_required
def profile_password_edit(request):
    """
    Renders and processes password edit page, containing three fields;
    1.current password 2.new password 3.confirm password. Password must satisfy
    the following criteria for it to be saved to database:
        - Must not be the same as the current password
        - Minimum password length of 14 characters.
        - Must use of both uppercase and lowercase letters
        - Must include of one or more numerical digits
        - Must include of special characters, such as @, #, $
        - Cannot contain the username or parts of thde user’s full name, such
        as his first name
    """

    try:
        profile = models.Profile.objects.get(user=request.user)
    except models.Profile.DoesNotExist:
        profile = models.Profile.objects.create(user=request.user)

    if request.method == 'POST':
        # check if user is currently logged in before proceeding
        if not user.is_active:
            messages.error(
                request,
                "User must be logged in to change password"
            )

            return HttpResponseRedirect(reverse('home'))

        form = forms.ChangePasswordForm(
            request.POST,
            user=user,
            profile=profile)

        if form.is_valid():
            user.set_password(form.cleaned_data['new_password'])
            user.save()

            # re-auth user to circumvent force log-out issue
            user = authenticate(
                username=user,
                password=form.cleaned_data['new_password']
            )

            login(request, user)

            messages.success(
                request,
                "Password change is successful!"
            )

            return HttpResponseRedirect(reverse('profile_view'))

    return render(request, 'profile_password_edit.html', {
        'form': form
    })
