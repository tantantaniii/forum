from django.urls import path
from . import views

urlpatterns = [
    path('', views.branch_list, name='branch_list'),
    path('branch/<int:branch_id>/', views.branch_detail, name='branch_detail'),
    path('branch/create/', views.create_branch, name='create_branch'),
    path('branch/<int:parent_id>/create-subbranch/', views.create_branch, name='create_subbranch'),
    path('topic/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    path('topic/<int:topic_id>/post/', views.post_message, name='post_message'),
    path('branch/<int:branch_id>/create-topic/', views.create_topic, name='create_topic'),
]