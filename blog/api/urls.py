from django.urls import include, path
from .import views 

from rest_framework.routers import DefaultRouter


router = DefaultRouter()


router.register('blog', views.BlogViewSet, basename='blog')
 
urlpatterns = [
      path('', include(router.urls)),
#     path('blog/<int:pk>/', views.URDBlog.as_view()),
#     path('blog/', views.LCBlogList.as_view()),
#     path('post/', views.blog),
#     path('post/<int:id>/', views.blog)
]