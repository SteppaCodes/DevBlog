
from django.shortcuts import render, get_object_or_404, redirect

from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .forms import EmailPostForm
from .models import Post

def posts(request):
    qs = Post.published.all()
    # Paginqtor class queries posts and return the number of posts specified
    #which is 5 
    paginator = Paginator(qs, 3)
    #Gets the request page number, and sets it to 1 if the page is 
    #not in the  HTTP header
    page_number = request.GET.get('page', 1)

    #Return the posts in the paginator
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        #catches an epty page for the instance where our paginator--
        #  does not have data up to the number of pages requested, 
        # then display the last page in the pagiaator
        posts = paginator.page(paginator.num_pages)

    except PageNotAnInteger:
        #Catches errors where the page entered is not an integer and renders the first page
        posts = paginator.page(1)

    context = {
        "posts":posts,
        "page":page_number
    }
    
    return render(request,'devblog/posts/list.html',context)

def post_detail(request, id):
    post = get_object_or_404(Post, id=id, 
                             status=Post.Status.PUBLISHED)

    context= {
        "post": post
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
 
        context = {
            'form':form,
            'post':post
        }

    return render(request, 'devblog/posts/share.html',{'form':form,
            'post':post}
        )

