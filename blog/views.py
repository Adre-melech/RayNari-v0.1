from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog, Comment
from .forms import CommentForm


def blog_home(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'blog/index.html', {'blogs': blogs})


def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'blog/list.html', {'blogs': blogs})


def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    # Increment view count only on GET requests
    if request.method == 'GET':
        blog.view_count += 1
        blog.save(update_fields=['view_count'])

    comments = blog.comments.filter(parent__isnull=True).order_by('-created_at')
    form = CommentForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.blog = blog
        parent_id = request.POST.get('parent_id')
        if parent_id:
            comment.parent_id = int(parent_id)
        comment.save()
        return redirect('blog:detail', pk=pk)

    return render(request, 'blog/detail.html', {
        'blog': blog,
        'comments': comments,
        'form': form,
    })