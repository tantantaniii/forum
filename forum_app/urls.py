from django.urls import path
from . import views

urlpatterns = [
    path('', views.BranchListView.as_view(), name='branch_list'),
    path('branch/<int:pk>/', views.BranchDetailView.as_view(), name='branch_detail'),
    path('branch/create/', views.BranchCreateView.as_view(), name='create_branch'),
    path('branch/<int:parent_id>/create-subbranch/', views.BranchCreateView.as_view(), name='create_subbranch'),

    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.LogoutConfirmView.as_view(), name='logout_confirm'),
    path('logout/action/', views.logout_action, name='logout_action'), 
    path('register/', views.RegisterView.as_view(), name='register'),
]