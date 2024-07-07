from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import  Post
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.auth.models import User

from .forms import CommentForm, EmailPostForm, SearchForm
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank
)

from django.shortcuts import render, redirect
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from actions.utils import create_action

import redis
from django.conf import settings


r = redis.Redis(
    host=settings.REDIS_HOST, 
    port=settings.REDIS_PORT, 
    password=settings.REDIS_PASSWORD,
    decode_responses=True
)


# from django.core.cache import caches

# cache = caches['default']



@login_required
@require_POST
def blog_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post.users_like.add(request.user)
                create_action(request.user, 'like', post)
            else:
                post.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except post.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # Do not overwrite the slug if it's already set
            if not post.slug:
                post.slug = slugify(post.title)
            post.save()
            form.save_m2m()
            create_action(request.user, 'create a new blog', post)
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()
    return render(request, 'blog/create_form.html', {'form': form})

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = (
                Post.published.annotate(
                    search=SearchVector('title', 'body'),
                )
                .filter(search=query)
            )
    return render(
        request,
        'blog/post/search.html',
        {
            'form': form,
            'query': query,
            'results': results
        }
    )


# def post_search(request):
#     form = SearchForm()
#     query = None
#     results = []
#     if 'query' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             search_vector = SearchVector('title', weight='A'
#             ) + SearchVector('body', weight='B')
#             search_query = SearchQuery(query)
#             results = (
#                 Post.published.annotate(
#                     similarity=TrigramSimilarity('title', query),
#                 )
#                 .filter(similarity__gt=0.1)
#                 .order_by('-similarity')
#             )
#     return render(
#         request,
#         'blog/post/search.html',
#         {
#             'form': form,
#             'query': query,
#             'results': results
#         }
#     )


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    # print(request.user)
    user = User.objects.get(username = request.user)
    # print(dir(user))
    # print(user.email)
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # print(cd)
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']}) "
                f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent = True
            # ... send email
    else:
        form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent
        }
    )


# class PostListView(ListView):
#     """
#     Alternative post list view
#     """
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day)
    
    # Check if the cache key exists; if not, set it with an initial value of 0
    total_views = r.incr(f'post:{post.id}:views')

    # increment image ranking by 1
    r.zincrby('post_ranking', 1, post.id)
    
    
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()
    
     # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    # print(post_tags_ids)
    # print(post_tags_ids[0])
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids
    ).exclude(id=post.id)
    similar_posts = similar_posts.annotate(
        same_tags=Count('tags')
    ).order_by('-same_tags', '-publish')[:4]
    
    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form,
            'similar_posts': similar_posts,
            'total_views': total_views
        }
    )

@login_required
def post_ranking(request):
    # get image ranking dictionary
    post_ranking = r.zrange(
        'post_ranking', 0, -1,
        desc=True
    )[:10]
    post_ranking_ids = [int(id) for id in post_ranking]
    # get most viewed images
    most_viewed = list(
        Post.objects.filter(
            id__in=post_ranking_ids
        )
    )
    most_viewed.sort(key=lambda x: post_ranking_ids.index(x.id))
    return render(
        request,
        'blog/post/ranking.html',
        { 'most_viewed': most_viewed}
    )
    
    
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.name = request.user
        comment.post = post
        # Save the comment to the database
        comment.save()
        return redirect(post.get_absolute_url())
    return render(
        request,
        'blog/post/comment.html',
        {
            'post': post,
            'form': form,
            'comment': comment
        }
    )

def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer get the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range get last page of results
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        'blog/post/list.html',
        {
            'posts': posts,
            'tag': tag
        }
    )
