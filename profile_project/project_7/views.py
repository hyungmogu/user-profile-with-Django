from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from accounts import forms, models


def home(request):
    return render(request, 'home.html')


@login_required
def profile_page(request):
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

            return HttpResponseRedirect(reverse('profile'))

    return render(request, 'profile.html', {
        'form': form
    })