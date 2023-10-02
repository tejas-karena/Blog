from django.http import HttpResponseRedirect
from django.shortcuts import render
from blogpost.models import Post, Comment, User
from django.views.generic import DetailView, ListView, TemplateView, CreateView
from .forms import SignUpForm, BlogAddForm, CommentForm, SearchForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import Count


class home(TemplateView):
    template_name = "blogpost/home.html"


class BlogList(ListView):
    model = Post    
    template_name = "blogpost/blog_list.html"
    context_object_name = "blog_list"
    paginate_by = 6


class AuthorDetail(DetailView):
    model = User
    template_name = "blogpost/author_detail.html"
    context_object_name = "author"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.object
        context["data"] = author.posts.all()
        return context


class BlogDetail(DetailView):
    model = Post
    template_name = "blogpost/blog_detail.html"
    context_object_name = "content"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        context["comments"] = post.comments.all()
        return context


class CommentFun(LoginRequiredMixin, View):
    template_name = "blogpost/comments.html"

    def get(self, request, **kwargs):
        uname = self.request.user.first_name
        blog_id = kwargs["pk"]
        title = Post.objects.get(pk=blog_id).title
        form = CommentForm()
        context = {"id": blog_id, "title": title, "form": form, "uname": uname}
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        blog_id = kwargs["pk"]
        content = request.POST.get("comment")
        if content:
            Comment.objects.create(
                commentblog_id=blog_id,
                comment=content,
                username=request.user,
            )
        return HttpResponseRedirect(reverse("blog-detail", kwargs={"pk": blog_id}))


class AuthorList(ListView):
    model = User
    template_name = "blogpost/author_list.html"
    context_object_name = "author_list"
    paginate_by = 5

    def get_queryset(self):
        queryset = User.objects.annotate(num_posts=Count("posts")).filter(
            num_posts__gt=0
        )
        return queryset


class Signup(CreateView):
    model = User
    template_name = "blogpost/sign_up.html"
    form_class = SignUpForm
    success_url = reverse_lazy("login")

    def get(self, request, **kwargs):
        form = SignUpForm()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            fm.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return HttpResponseRedirect("/accounts/register/")


class BlogAdd(LoginRequiredMixin, View):
    template_name = "blogpost/blog_add.html"
    form_class = BlogAddForm

    def get(self, request, **kwargs):
        context = {
            "author": self.request.user.first_name,
            "form": self.form_class(),
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = BlogAddForm(request.POST)
        if form.is_valid():
            form.instance.author = self.request.user
            form.save()
            return HttpResponseRedirect(
                reverse("author-detail", kwargs={"pk": request.user.id})
            )
        else:
            return render(request, self.template_name, {"form": form})


class SearchFun(ListView):
    template_name = "blogpost/search.html"
    model = Post
    context_object_name = "blog_list"

    def get(self, request):
        form = SearchForm()
        return render(request, "home", {"form": form})

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            word = form.cleaned_data["search"]
            queryset = Post.objects.filter(title__icontains=word)
            return render(request, self.template_name, {"blog_list": queryset})
        else:
            return render(request, "home", {"form": form})
