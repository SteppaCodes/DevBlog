from django.urls import path
from .views import (posts, post_detail, 
                    post_share, post_comment,
                    tag_page
                    )


urlpatterns = [
    path('posts/',posts, name='posts'),
    path('post/<int:id>/',post_detail, name='post_detail'),
    path('<int:id>/share', post_share, name='post_share'),

    path('<int:id>/comment', post_comment, name='post_comment'),
    path('posts/<int:tag_id>', posts, name='tag_page')
]

