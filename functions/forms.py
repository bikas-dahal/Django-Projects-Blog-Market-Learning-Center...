from django import forms

class DownloadForm(forms.Form):
    video_url = forms.URLField(label='Enter the YouTube Video URL')
