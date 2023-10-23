from django.shortcuts import render, get_object_or_404

from .models import Post

def posts(request):
    posts = Post.published.all()
    print(posts)

    context = {
        posts:"posts",
    }
    
    return render(request,'devblog/posts/list.html',context)

def post_detail(request, id):
    post = get_object_or_404(Post, id=id, 
                             status=Post.Status.PUBLISHED)

    context= {
        post: 'post'
    }
    return render(request,'devblog/posts/detail.html',context)