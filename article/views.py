from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DeleteView, DetailView
from django.views.generic.edit import UpdateView, CreateView
from . models import Article

# Create your views here.
class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
    
    
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html' 

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list') 
    
    
    def test_func(self):
        article = self.get_object()
        if self.request.user == article.author:
            return True
        return False
    

class ArticleEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ('title', 'content') 
    template_name = 'article_edit.html'
    
    def test_func(self):
        article = self.get_object()
        if self.request.user == article.author:
            return True
        return False
    
    
    
class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'article_create.html'
    fields = ['title','content', ]
    login = 'login'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    


    