
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),         
    path('devblog/', include(('apps.blog.urls', 'blog'), namespace='blog'))
]
                       