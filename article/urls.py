from django.urls import path
from . import views

urlpatterns = [
    path('articles', views.ArticleListView.as_view(), name='article_list'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('article/<int:pk>/edit', views.ArticleEditView.as_view(), name='article_edit'),
    path('article/<int:pk>/delete', views.ArticleDeleteView.as_view(), name='article_delete'),
    path('article/new', views.ArticleCreateView.as_view(), name='article_new'),
]
