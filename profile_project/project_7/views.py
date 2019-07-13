from django.shortcuts import render

from accounts import forms


def home(request):
    return render(request, 'home.html')


# TODO: Restrict access to profile_page to logged in users only
# NOTE: Currently accessible by typing 'http://127.0.0.1:8000/profile/1/'
def profile_page(request, user_pk):
    # TODO: get information about the user and prepopulate here
    form = forms.ProfileForm()

    if request.method == 'POST':
        form = forms.ProfileForm(request.POST)

        if form.is_valid():
            form.save()

            # TODO: Replace HttpResponseRedirect('home') with something more proper
            return HttpResponseRedirect('home')
    return render(request, 'profile.html', {
        'form': form
    })