from django.contrib import admin
from django.urls import path, include
from bulletin.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, post_reply, ReplyListView, accept_response, ReplyDeleteView


urlpatterns = [
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/create', PostCreateView.as_view(), name = 'post_create'),
    path('post/<int:pk>/edit', PostUpdateView.as_view(), name = 'post_edit'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name = 'post_delete'),
    path('post/<int:pk>/reply', post_reply, name='post_reply'),
    path('replies/', ReplyListView.as_view(), name='reply_list'),
    path('reply/<int:pk>/accept/', accept_response, name='accept_response'),
    path('replies/<int:pk>/delete', ReplyDeleteView.as_view(), name='reply_delete'),
]
 