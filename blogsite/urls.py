"""
URL configuration for blogsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include    # add include to pass control to another URL file (other than the admin, here we are passing it to urls in the posts app.)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/',  auth_views.LoginView.as_view(template_name='posts/login.html'),
                    name='login'),
            
        #Addition: Django's LoginView handles reading the form, validating credentials, creating a session.
                   #We are writing template name to route it which template to render via "login.html"
    path('logout/', auth_views.LogoutView.as_view(),
                    name='logout'),
        #Addition: LogoutView destroys the session created and redirects to LOGOUT_REDIRECT_URL = '/login/'
    path('', include('posts.urls')), #
]
