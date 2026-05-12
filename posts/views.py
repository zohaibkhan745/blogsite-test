from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.contrib.auth.decorators import login_required
# We are importing login_required (a decorator)

from .ai_helper import generate_summary


def post_list(request): #Reading is PUBLIC, Everyone is WELCOMED
    posts = Post.objects.all().order_by('-date')
    return render(request, 'posts/list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/detail.html', {'post': post})

@login_required
# Authentication Guard — User must be logged in to create
# A decorator wraps the function with extra functionality before the function body runs.                                          
def post_create(request):
    if request.method == 'POST':
        Post.objects.create(
            author   = request.user,
            title    = request.POST['title'],
            category = request.POST['category'],
            content  = request.POST['content'],
        )
        return redirect('post_list')
    return render(request, 'posts/form.html')

# ── Our two layer Authentication + Authorization Guard 
@login_required                                             
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Authorization: only the author may edit their owned posts        
    if post.author != request.user:
        return redirect('post_list')

    if request.method == 'POST':
        post.title    = request.POST['title']
        post.category = request.POST['category']
        post.content  = request.POST['content']
        post.save()
        return redirect('post_list')
    return render(request, 'posts/form.html', {'post': post})

@login_required                                    
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Authorization: only the author may delete their created posts
    if post.author != request.user:
        return redirect('post_list')

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'posts/confirm_delete.html', {'post': post})




# ── We are adding this function at the very bottom of views.py to call AI through out helper AI
# What if we want to grant this summary feature to any visitor?
@login_required
def post_summary(request, pk):
    """
    Fetch a post, send its content to the Groq LLM via ai_helper.py,
    and render the AI-generated summary on a dedicated page.

    Protected by @login_required so only logged-in users can
    trigger API calls (prevents anonymous quota abuse).
    """
    post = get_object_or_404(Post, pk=pk)

    # This single line calls Groq through our helper module.
    # The view does not know about API keys, HTTP requests,
    # or the Groq library — all that is inside ai_helper.py.
    summary = generate_summary(post.content)

    return render(request, 'posts/summary.html', {
        'post':    post,
        'summary': summary,
    })