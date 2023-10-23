from django.urls import path
from .views import posts, post_detail


urlpatterns = [
    path('posts',posts, name='posts'),
    path('<int:id>/',post_detail, name='post_detail')
]

