
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

from django.contrib.postgres.search import SearchVector

from .forms import EmailPostForm, CommmentForm, SearchForm
from .models import Post,Tag

#TODO: FIx Search template issue...add search form to base.html and handle search from there
#TODO: Current problem -> the base.html does not read the context variable

def search(request):
    query= None
    results = []
    form = SearchForm()

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                search=SearchVector('title', 'body')
            ).filter(search=query)
    context = {
        'form':form,
        'results':results,
        'query':query
    }
    return render(request, 'devblog/posts/search.html', context)


def posts(request, tag_id=None):
    #Get all available tags
    tags = Tag.objects.all()
    #Get all published posts
    qs = Post.published.all()

    #Check if a tag id was supplied from the url
    if tag_id:
        #Retrieve the tag clicked from the tag object
        tag = tags.get(id=tag_id)
        #set the queryset for the pagination to posts with_
        # the tag specified 
        post_list = qs.filter(tags__in = [tag])
    # Else let the post be all posts in the database
    else:  
        post_list = qs
    # Paginator class queries posts and return the number of posts specified
    #which is 5 
    paginator = Paginator(post_list, 5)
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
        "page":page_number,
        "tags":tags
    }
    
    return render(request,'devblog/posts/list.html',context)

def post_detail(request, id):
    post = get_object_or_404(Post, id=id, 
                             status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)
    tags = post.tags.all()
    form = CommmentForm()

    # get the ids of the tags used in the post,
    #.values_list creates a list of values from the specified field (in this case....id)
    # flat=True -> Gets single valuesinstead of tuples
    post_tag_ids = post.tags.values_list('id', flat=True)
    #filter all published posts and get posts with the same tags- 
    #Use the distinct to only return one of each result
    similar_posts = Post.published.filter(tags__in=post_tag_ids).exclude(id=post.id).distinct()
    # Count the number of tags that are the same in similar posts -
    # and return them from highest to lowest
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')
    

    context= {
        "post": post,
        'comments':comments,
        'tags':tags,
        'similar_posts':similar_posts,
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

