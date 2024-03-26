from django.contrib.auth.models import User
from django.urls import path
from user_auth.views import login_view, home_view, register_view, logout

urlpatterns = [
    path("", home_view, name="store"),
    path('login', login_view, name='login'),
    path('signup', register_view),
    path('logout', logout, name="logout")

]
