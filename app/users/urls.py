from django.urls import path

from .views import RegisterView, CustomLoginView, CustomLogoutView, ProfileView


app_name = 'users'

urlpatterns = [
    path('registration/', RegisterView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('<str:slug>/', ProfileView.as_view(), name='profile')
]
