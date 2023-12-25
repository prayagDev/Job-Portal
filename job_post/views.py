from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from job_post.models import Post, Category
from job_post.forms import PostForm
from django.db.models import Q
from django.urls import reverse, reverse_lazy
# Create your views here.

def home(request):
    category=Category.objects.all()
    recent_posts=Post.objects.all().order_by("-created_date")
    paginator = Paginator(recent_posts, 1)  # Show 10 posts per page
    page = request.GET.get('page')
    try:
        recent_posts = paginator.page(page)
    except PageNotAnInteger:
        recent_posts = paginator.page(1)
    except EmptyPage:
        recent_posts = paginator.page(paginator.num_pages)
    context={'recent_posts':recent_posts, 'category':category}
    return render(request, "job_post\home.html", context)

def category_post(request, name):
    category=Category.objects.get(name=name)
    c_post=Post.objects.filter(description__icontains=category).order_by("-created_date")
    context={'c_post':c_post}
    return render(request, "job_post\category_post.html", context)

def search_post(request):
    title=request.GET.get('title')
    experience=request.GET.get('experience')
    location=request.GET.get('location')
    posts=Post.objects.filter(Q(title__icontains=title) | Q(content__icontains=location) | Q(content__icontains=experience) |Q(description__icontains=experience) | Q(description__icontains=location))
    context={'posts':posts, 'keyword':{'title':title, 'experience':experience, 'location':location}}
    return render(request, "job_post\search_post.html", context)

def post_detail(request, slug):
    my_post=Post.objects.get(slug=slug)
    context={'my_post':my_post}
    return render(request, "job_post\post_detail.html", context)

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class=PostForm
    template_name = 'job_post/post_create.html'
    def form_valid(self, form):
        form.instance.employer = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('read_post')
    
class PostRead(LoginRequiredMixin, ListView):
    model = Post 
    template_name = 'job_post/post_read.html' 
    context_object_name = 'object_list'

    def get_queryset(self):
        return Post.objects.filter(employer=self.request.user)
    
class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'job_post/post_delete.html'
    success_url = reverse_lazy('read_post')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(employer=self.request.user)
    
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'job_post/post_create.html'
    form_class = PostForm  
    success_url = reverse_lazy('read_post') 

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(employer=self.request.user)