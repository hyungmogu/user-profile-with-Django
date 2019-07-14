from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from accounts import forms


def home(request):
    return render(request, 'home.html')


# TODO: Create a 'submit' button on view that performs request.POST action on save
@login_required
def profile_page(request):
    user = get_object_or_404(User, pk=request.user.pk)
    form = forms.ProfileForm(instance=user)

    if request.method == 'POST':
        form = forms.ProfileForm(request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('home'))

    return render(request, 'profile.html', {
        'form': form
    })