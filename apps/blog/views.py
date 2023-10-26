from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

from .forms import EmailPostForm, CommmentForm
from .models import Post, Comment

def posts(request):
    posts = Post.published.all()
    print(posts)

    context = {
        "posts":posts,
    }
    
    return render(request,'devblog/posts/list.html',context)

def post_detail(request, id):
    post = get_object_or_404(Post, id=id, 
                             status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)
    form = CommmentForm()
    context= {
        "post": post,
        'comments':comments,
        'form':form
    }
    return render(request,'devblog/posts/detail.html',context)

def post_share(request, id):
    post = get_object_or_404(Post, id=id, status= Post.Status.PUBLISHED)
    form = EmailPostForm()
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #use post's url to build a url thatd lead to the post from mail
            post_url = request.build_absolute_uri(post.get_absolute_url)
            subject = f"{cd['name']} suggest you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comment: {cd['comment']}"

            send_mail(subject, message, 'Steppacodes@devblog.com', [cd['to']], fail_silently=False)
            sent = True
            #return redirect('post', post.id)
        else:
            form = EmailPostForm()                                                                    
    return render(request, 'devblog/posts/share.html',{
            'form':form,
            'post':post,
            'sent':sent
            }
        )

@require_POST
def post_comment(request, id):
    post = get_object_or_404(Post,id=id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommmentForm(data=request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    print(comment)

    context = {
        'form':form,
        'post':post,
        'comment':comment
    }
    return render(request, 'devblog/posts/comment.html', context)

