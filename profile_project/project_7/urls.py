"""project_7 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    url(r'^profile/password/edit$', views.profile_password_edit,
        name='profile_password_edit'),
    url(r'^profile/edit', views.profile_edit,
        name='profile_edit'),
    url(r'^profile/', views.profile_view,
        name='profile_view'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^$', views.home, name='home')
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
