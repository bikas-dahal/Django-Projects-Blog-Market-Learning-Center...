"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap, TagSitemap

from django.conf import settings
from django.conf.urls.static import static
from courses.views import CourseListView


sitemaps = {
    'posts': PostSitemap,
    'tags': TagSitemap,
}

urlpatterns = [
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    # path('accounts/', include('allauth.urls')),
    path('account/', include('account.urls')),
    path( 
        'social-auth/',
        include('social_django.urls', namespace='social')
    ),

    path('images/', include('images.urls', namespace='images')),

    # path('accounts/', include('accounts.urls')),
    path('blog/', include('blog.urls', namespace='blog')),

    path('', include('functions.urls')),
    path('weather', include('weather.urls')),
    path('summernote/', include('django_summernote.urls')),
    # path('', include('chat.urls')),

    # shop
    path('payment/', include('payment.urls', namespace='payment')),
    path('shop/', include('shop.urls', namespace='shop')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('coupons/', include('coupons.urls', namespace='coupons')),

    # courses
    path('course/', include('courses.urls')),
    path('courses', CourseListView.as_view(), name='course_list'),
    path('students/', include('students.urls')),
    path('api/', include('courses.api.urls', namespace='api')),
    path('chat/', include('chat.urls', namespace='chat')),

]
if settings.DEBUG:
    import debug_toolbar
    # urlpatterns += [
    #     path('__debug__/', include(debug_toolbar.urls)),
    # ]
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )