from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Branch, Topic, Message
from .forms import MessageForm, BranchForm, TopicForm

def branch_list(request):
    branches = Branch.objects.filter(parent_branch__isnull=True).prefetch_related('subbranches')
    return render(request, 'forum/branch_list.html', {'branches': branches})

def branch_detail(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    subbranches = branch.subbranches.all()
    topics = branch.topics.all()
    return render(request, 'forum/branch_detail.html', {
        'branch': branch,
        'subbranches': subbranches,
        'topics': topics
    })

def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    messages = topic.messages.all().order_by('created_at')
    form = MessageForm(request.POST or None, topic=topic)  # ← ДОБАВЬ topic=topic

    if request.method == 'POST' and form.is_valid():
        message = form.save(commit=True)  # ← теперь .save() работает!
        return redirect('topic_detail', topic_id=topic.id)

    return render(request, 'forum/topic_detail.html', {
        'topic': topic,
        'messages': messages,
        'form': form
    })

@login_required
def post_message(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                topic=topic,
                author=request.user,
                content=content
            )
        return redirect('topic_detail', topic_id=topic.id)
    return redirect('topic_detail', topic_id=topic.id)

@login_required
def create_branch(request, parent_id=None):
    parent_branch = None
    if parent_id:
        parent_branch = get_object_or_404(Branch, id=parent_id)

    if request.method == 'POST':
        form = BranchForm(request.POST, parent_branch=parent_branch)
        if form.is_valid():
            branch = form.save(commit=False)
            branch.author = request.user  
            branch.save()
            return redirect('branch_detail', branch.id)
    else:
        form = BranchForm(parent_branch=parent_branch)

    return render(request, 'forum/create_branch.html', {
        'form': form,
        'parent_branch': parent_branch
    })

@login_required
def create_topic(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)

    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.branch = branch
            topic.author = request.user
            topic.save()
            return redirect('topic_detail', topic.id)
    else:
        form = TopicForm(initial={'branch': branch})

    return render(request, 'forum/create_topic.html', {
        'form': form,
        'branch': branch
    })