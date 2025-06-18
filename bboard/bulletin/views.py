from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Post, Reply
from .forms import PostForm
from .filters import ReplyFilter

class PostListView(ListView):
    model = Post
    template_name = 'bulletin/posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'bulletin/post_detail.html'
    context_object_name = 'post'
    
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'bulletin/post_edit.html'
    context_object_name = 'post'
    success_url = reverse_lazy('post_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'bulletin/post_edit.html'
    context_object_name = 'post'
    success_url = reverse_lazy('post_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'bulletin/post_delete.html'
    success_url = reverse_lazy('post_list')
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

@login_required 
def post_reply(request, pk):
    post = Post.objects.get(pk=pk)

    if request.method == 'POST':
        content = request.POST.get('content')
        reply = Reply(content=content, sender=request.user, recipient=post.author, post=post)
        reply.save()
        messages.success(request, 'Вы успешно откликнулись на объявление.')
        return redirect('post_detail', pk=pk)
    return render(request, 'bulletin/post_reply.html', {'post': post})

class ReplyListView(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'bulletin/reply_list.html'
    context_object_name = 'replies'
    paginate_by = 10
    filterset_class = ReplyFilter
    
    def get_queryset(self):
        self.filterset = ReplyFilter(self.request.GET, queryset=Reply.objects.filter(recipient=self.request.user))
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

def accept_response(request, pk):
    reply = Reply.objects.get(pk=pk)
    if request.method == 'POST':
        reply.is_accepted = True
        reply.save()
        messages.success(request, 'Отклик принят.')
        return redirect('reply_list')
    return render(request, 'bulletin/reply_list.html', {'reply': reply})

class ReplyDeleteView(LoginRequiredMixin, DeleteView):
    model = Reply
    template_name = 'bulletin/reply_delete.html'
    success_url = reverse_lazy('reply_list')
    
    def get_queryset(self):
        return Reply.objects.filter(recipient=self.request.user)