from django import forms
from .models import Comment

from django import forms
from .models import Post
from taggit.forms import TagWidget

from django import forms
from .models import Post
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class PostForm(forms.ModelForm):
    class Meta:
        
        model = Post
        fields = ['title', 'slug', 'body', 'tags', 'status']
        widgets = {
            'body': SummernoteWidget(),
            'slug': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
        initial = {
            'status': 'PB',  # Set the default status to 'Published'
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
        

class SearchForm(forms.Form):
    query = forms.CharField()
    
    

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea
    )
    
