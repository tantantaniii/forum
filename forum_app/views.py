from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from .models import Branch, Topic, Message
from .forms import BranchForm, TopicForm, MessageForm


class BranchListView(ListView):
    model = Branch
    template_name = 'forum/branch_list.html'
    context_object_name = 'branches'

    def get_queryset(self):
        return Branch.objects.filter(parent_branch__isnull=True).prefetch_related('subbranches')


class BranchDetailView(DetailView):
    model = Branch
    template_name = 'forum/branch_detail.html'
    context_object_name = 'branch'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        branch = self.object
        context['subbranches'] = branch.subbranches.all()
        context['topics'] = branch.topics.all()
        return context


class BranchCreateView(LoginRequiredMixin, CreateView):
    model = Branch
    form_class = BranchForm
    template_name = 'forum/create_branch.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        parent_id = self.kwargs.get('parent_id')
        if parent_id:
            kwargs['parent_branch'] = get_object_or_404(Branch, id=parent_id)
        return kwargs

    def get_success_url(self):
        return reverse_lazy('branch_detail', kwargs={'pk': self.object.pk})


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'forum/create_topic.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'branch': self.kwargs['branch_id']}
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.branch = get_object_or_404(Branch, id=self.kwargs['branch_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('topic_detail', kwargs={'pk': self.object.pk})


class TopicDetailView(DetailView):
    model = Topic
    template_name = 'forum/topic_detail.html'
    context_object_name = 'topic'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = self.object
        context['messages'] = topic.messages.all().order_by('created_at')
        context['form'] = MessageForm(topic=topic)  
        return context

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'forum/topic_detail.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['topic'] = get_object_or_404(Topic, id=self.kwargs['topic_id'])
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('topic_detail', kwargs={'pk': self.kwargs['topic_id']})