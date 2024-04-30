from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from pytube import YouTube
import requests
import logging
from django.http import JsonResponse
from pytube import YouTube
import requests

# Create your views here.
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
