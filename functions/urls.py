from django.urls import path

from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('yt_home/',views.homePage,name="yt_home"),
    path('details/',views.detailsFunction,name="details"),
    path('download/',views.downloadFunction,name="download"),
]