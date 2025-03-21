from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from .views import homepage, signup
urlpatterns = [path('', homepage, name='home'),
               path('signup/', signup, name='signup'),
                path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),
                path('logout/', LogoutView.as_view(), name='logout')]