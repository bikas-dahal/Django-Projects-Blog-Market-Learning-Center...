from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from pytube import YouTube
import requests
import logging
from django.http import JsonResponse
from pytube import YouTube
import requests

# Create your views here.

def home(request):
    return render(request, 'home.html')


# views.py# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserInteraction
import google.generativeai as genai
from decouple import config

@login_required
def get_answer(request):
    context = {}
    if request.method == 'POST':
        question = request.POST.get('question')
        
        # Save the question in the session for personalization
        if 'questions' not in request.session:
            request.session['questions'] = []
        request.session['questions'].append(question)
        request.session.modified = True
        
        # Interact with the Gemini API
        API_KEY = config('GEMINI_API_KEY')
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(question)
        
        # Save the interaction in the database
        UserInteraction.objects.create(user=request.user, question=question, answer=response.text)
        
        context['answer'] = response.text
        context['question'] = question
        
    # Retrieve past interactions for personalization
    past_interactions = UserInteraction.objects.filter(user=request.user).order_by('-timestamp')[:5]
    context['past_interactions'] = past_interactions

    return render(request, 'search_form.html', context)



def homePage(request):
    return render(request, 'functions/download_page.html')

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds)



# Set up logging
logger = logging.getLogger(__name__)

def detailsFunction(request):
    # Check for AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        url = request.POST.get('url')
        
        # Validate the URL
        if not ('youtube.com' in url or 'youtu.be' in url):
            return JsonResponse({'status': 201, 'value': 'Please enter a correct YouTube URL'}, status=400)
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
            
            if "Video unavailable" in response.text:
                return JsonResponse({'status': 201, 'value': 'Video not available'}, status=404)
            
            yt = YouTube(url)
            # Extract video details
            data = {
                'status': 200,
                'title': yt.title,
                'views': yt.views,
                'duration': convert(yt.length),
                'desc': yt.description,
                'rating': yt.rating,
                'url_code': url.split('=')[1] if '=' in url else url.split('/')[3],
                'url': url
            }
            return JsonResponse(data)
        except requests.HTTPError as e:
            logger.error(f'HTTPError for URL {url}: {e}')
            return JsonResponse({'status': 201, 'value': 'Failed to retrieve video details'}, status=500)
        except Exception as e:
            logger.error(f'Error in detailsFunction for URL {url}: {e}')
            return JsonResponse({'status': 201, 'value': 'An error occurred'}, status=500)
    else:
        return JsonResponse({'status': 400, 'value': 'Invalid request'}, status=400)


def downloadFunction(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        url = request.GET['url']
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download()
        return JsonResponse({'status': 'Download completed!!'})
    else:
        return JsonResponse({'status': 'Download Failed'})
