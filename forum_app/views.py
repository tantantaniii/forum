from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Branch, Message
from .forms import (
    CustomUserCreationForm,
    BranchForm,
    MessageForm
)


# === АВТОРИЗАЦИЯ ===

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('branch_list')


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


# === СТРАНИЦА ПОДТВЕРЖДЕНИЯ ВЫХОДА ===

class LogoutConfirmView(TemplateView):
    template_name = 'registration/logout.html'


def logout_action(request):
    """Выполняет выход при POST-запросе"""
    if request.method == 'POST':
        logout(request)
        return redirect('branch_list')
    # Если GET — перенаправляем на подтверждение
    return redirect('logout_confirm')


# === ФОРУМ ===

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
        if branch.parent_branch:
            # Это тема (подветка) — показываем сообщения
            context['messages'] = branch.messages.select_related('author').order_by('created_at')
            context['form'] = MessageForm()
        else:
            # Это корневая ветка — показываем подветки (темы)
            context['subbranches'] = branch.subbranches.all()
        return context

    def post(self, request, *args, **kwargs):
        branch = self.get_object()
        if not branch.parent_branch:
            return redirect('branch_detail', pk=branch.pk)

        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.branch = branch
            message.author = request.user
            message.save()
            return redirect('branch_detail', pk=branch.pk)

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


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

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('branch_detail', kwargs={'pk': self.object.pk})