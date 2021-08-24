from django.shortcuts import (
    render, reverse, redirect, get_object_or_404
)
from .models import BlogPost, Comments
from .forms import CommentForm
from django.contrib import messages

from datetime import datetime


def view_blog(request):
    """ A view to return the index page """

    blogpost = BlogPost.objects.all()

    template = 'blog/blog.html'
    context = {
        'blogpost': blogpost,
    }

    return render(request, template, context)


def blog_detail(request, blog_id):
    """ A view to return the blog post """

    blogpost = get_object_or_404(BlogPost, pk=blog_id)
    comment = blogpost.comment.all()
    user = request.user

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.post_id = blogpost.id
                form.user = user
                form.timestamp = datetime.now()
                form.save()
                messages.success(
                    request,
                    'Your comment has been successfully posted!'
                )
                return redirect(reverse('blog_detail', args=[blogpost.id]))
            else:
                messages.error(
                    request,
                    'Your comment failed to post. \
                    Please check the form is valid and try again.'
                )
        else:
            messages.error(
                    request,
                    'You must log in to post a comment.'
                )
            return redirect(reverse('account_login'))
    else:
        form = CommentForm()

    context = {
        'form': form,
        'blogpost': blogpost,
        'comment': comment,
    }

    return render(request, 'blog/blog_detail.html', context)