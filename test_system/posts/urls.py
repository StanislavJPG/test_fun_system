from django.urls import path

from posts.views import AllPostsView, PostView

urlpatterns = [
    path('posts/all/', AllPostsView.as_view(), name='all_posts'),
    path('posts/<int:post_id>/', PostView.as_view(), name='post'),
    # path('posts/delete/<int:post_id>'),
]
