from django.urls import path


from . import views


urlpatterns = [
    # регистрация
    path('signup/', views.SignUp.as_view(), name='signup'),
]