"""foodgram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.flatpages import views
from django.conf.urls import handler404

handler404 = "recipes.views.page_not_found" # noqa


urlpatterns = [
    # раздел администратора
    path('admin/', admin.site.urls),
    # flatpages
    path('about/', include('django.contrib.flatpages.urls')),
    path('about-author/', views.flatpage,
         {'url': '/about-author/'}, name='about_author'),
    path('about-specs/', views.flatpage,
         {'url': '/about-specs/'}, name='about_specs'),
    # раздел авторизации
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    # раздел рецептов
    path('', include('recipes.urls')),
    # api фронтенда
    path('api/', include('api_frontend.urls'))
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
