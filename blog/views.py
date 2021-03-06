import datetime

from django.conf import settings
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.views.generic import ListView
from taggit.models import Tag

from blog import pager
from blog.forms import EmailPostForm, CommentForm, SearchForm
from blog.models import Post


def log(c):
    print(datetime.datetime.now(), c)


def post_list(request, tag_slug=None):
    all_posts = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        all_posts = all_posts.filter(tags__in=[tag])
        # todo delete
        # log(all_posts.query)
    paginator = Paginator(all_posts, settings.POSTS_PER_PAGE)
    page = request.GET.get('page', 1)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    page_obj = pager.Page(posts.number, paginator.num_pages)
    return render(request, 'blog/post/list.html', {
        'posts': posts,
        'page': page,
        'tag': tag,
        'page_obj': page_obj,
    })


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day)

    comment_form = CommentForm(request.POST or None)
    comments = post.comments.filter(active=True)
    new_comment = None
    # post method and valid
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.post = post
        new_comment.save()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # todo delete
    # log(similar_posts.query)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by(
        '-same_tags', '-publish')[:4]
    # todo delete
    # log(similar_posts.query)
    log(similar_posts.all())
    return render(
        request, 'blog/post/detail.html', {
            'post': post,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form,
            'similar_posts': similar_posts,
        })


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'],
                                                                   post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url,
                                                                     cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


def post_search(request):
    form = SearchForm(request.GET or None)
    query = None
    posts = None
    page_obj = None
    paginator = None
    if form.is_valid():
        query = form.cleaned_data['query']

        search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
        search_query = SearchQuery(query)
        posts = Post.published.annotate(rank=SearchRank(search_vector, search_query)).filter(
            rank__gte=0.3).order_by('-rank')
        paginator = Paginator(posts, settings.POSTS_PER_PAGE)
        page = request.GET.get('page', 1)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        page_obj = pager.Page(posts.number, paginator.num_pages)

    return render(request, 'blog/post/list.html', {
        'query': query,
        'paginator': paginator,
        'posts': posts,
        'page_obj': page_obj,
    })
