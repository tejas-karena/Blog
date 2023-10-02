"""
URL configuration for demo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from blogpost import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home.as_view(), name="home"),
    path("blog/", views.home.as_view(), name="home"),
    path("blog/blogs/", views.BlogList.as_view(), name="blog-list"),
    path("blog/<int:pk>/", views.BlogDetail.as_view(), name="blog-detail"),
    path("blog/blogger/<int:pk>/", views.AuthorDetail.as_view(), name="author-detail"),
    path("blog/bloggers/", views.AuthorList.as_view(), name="author-list"),
    path("blog/<int:pk>/create/", views.CommentFun.as_view(), name="comment"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register/", views.Signup.as_view(), name="sign-up"),
    path("add/<int:pk>/", views.BlogAdd.as_view(), name="blog-add"),
    path("blog/search/",views.SearchFun.as_view(), name="blog-search")
]
