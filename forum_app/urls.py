from django.urls import path
from . import views

urlpatterns = [
    path('', views.BranchListView.as_view(), name='branch_list'),
    path('branch/<int:pk>/', views.BranchDetailView.as_view(), name='branch_detail'),
    path('branch/create/', views.BranchCreateView.as_view(), name='create_branch'),
    path('branch/<int:parent_id>/create-subbranch/', views.BranchCreateView.as_view(), name='create_subbranch'),
    path('branch/<int:branch_id>/create-topic/', views.TopicCreateView.as_view(), name='create_topic'),
    path('topic/<int:pk>/', views.TopicDetailView.as_view(), name='topic_detail'),
    path('topic/<int:topic_id>/post/', views.MessageCreateView.as_view(), name='post_message'),
]