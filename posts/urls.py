from django.urls import path
from . import views

urlpatterns = [
    path('',               views.post_list,   name='post_list'),
    path('create/',        views.post_create, name='post_create'),
    path('<int:pk>/',      views.post_detail, name='post_detail'),
    path('<int:pk>/edit/', views.post_update, name='post_update'),
    path('<int:pk>/del/',  views.post_delete, name='post_delete'),
    path('<int:pk>/summary/', views.post_summary, name='post_summary'),  # NEW URL for AI integration
]
