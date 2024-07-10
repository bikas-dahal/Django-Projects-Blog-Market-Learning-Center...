from django.urls import include, path
from .import views 

 
urlpatterns = [
    path('stl/', views.LCBlogList.as_view()),
    path('post/', views.blog)
]