import os
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import re
from urllib.parse import parse_qs, urlparse
import yt_dlp

def home(request):
    return render(request, 'converter/home.html')

def extract_video_id(url):
    """Extract video ID from various YouTube URL formats."""
    if not url:
        return None
        
    # Handle youtu.be format
    if 'youtu.be' in url:
        return url.split('/')[-1]
        
    # Handle youtube.com format
    parsed_url = urlparse(url)
    if 'youtube.com' in parsed_url.netloc:
        query_params = parse_qs(parsed_url.query)
        return query_params.get('v', [None])[0]
        
    return None

def is_valid_youtube_url(url):
    """Check if the URL is a valid YouTube URL."""
    if not url:
        return False
        
    video_id = extract_video_id(url)
    return bool(video_id and len(video_id) == 11)

@csrf_exempt
def download(request):
    if request.method == 'POST':
        try:
            # Log the raw request body for debugging
            print("Request body:", request.body)
            
            data = json.loads(request.body)
            video_url = data.get('url')
            
            if not video_url:
                return HttpResponse(json.dumps({
                    'success': False,
                    'error': 'URL is required'
                }), status=400)
            
            if not is_valid_youtube_url(video_url):
                return HttpResponse(json.dumps({
                    'success': False,
                    'error': 'Invalid YouTube URL format'
                }), status=400)
            
            # Create downloads directory if it doesn't exist
            downloads_dir = os.path.join(settings.BASE_DIR, 'downloads')
            os.makedirs(downloads_dir, exist_ok=True)
            
            try:
                # Configure yt-dlp options
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': os.path.join(downloads_dir, '%(title)s.%(ext)s'),
                    'quiet': False,
                    'no_warnings': False,
                }
                
                print(f"Processing URL: {video_url}")
                
                # Download and convert the video
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Get video info first
                    print("Fetching video info...")
                    info = ydl.extract_info(video_url, download=False)
                    video_title = info.get('title', 'video')
                    print(f"Video title: {video_title}")
                    
                    # Download the video
                    print("Starting download...")
                    ydl.download([video_url])
                    
                    # Get the output filename
                    output_filename = f"{video_title}.mp3"
                    output_path = os.path.join(downloads_dir, output_filename)
                    
                    if not os.path.exists(output_path):
                        raise Exception("Failed to create MP3 file")
                    
                    print(f"Download completed: {output_path}")
                    
                    # Return the download URL
                    return HttpResponse(json.dumps({
                        'success': True,
                        'filename': output_filename,
                        'title': video_title
                    }))
                
            except Exception as e:
                error_message = str(e)
                print(f"YouTube Error: {error_message}")
                
                if "Video unavailable" in error_message:
                    return HttpResponse(json.dumps({
                        'success': False,
                        'error': 'This video is unavailable'
                    }), status=400)
                elif "Sign in to confirm your age" in error_message:
                    return HttpResponse(json.dumps({
                        'success': False,
                        'error': 'This video requires age verification'
                    }), status=400)
                elif "private video" in error_message.lower():
                    return HttpResponse(json.dumps({
                        'success': False,
                        'error': 'This video is private'
                    }), status=400)
                elif "copyright" in error_message.lower():
                    return HttpResponse(json.dumps({
                        'success': False,
                        'error': 'This video is not available due to copyright restrictions'
                    }), status=400)
                elif "age restricted" in error_message.lower():
                    return HttpResponse(json.dumps({
                        'success': False,
                        'error': 'This video is age restricted'
                    }), status=400)
                else:
                    return HttpResponse(json.dumps({
                        'success': False,
                        'error': f'Error processing video: {error_message}'
                    }), status=500)
            
        except json.JSONDecodeError:
            return HttpResponse(json.dumps({
                'success': False,
                'error': 'Invalid JSON data'
            }), status=400)
        except Exception as e:
            print(f"Error: {str(e)}")
            return HttpResponse(json.dumps({
                'success': False,
                'error': str(e)
            }), status=500)
    
    return HttpResponse(json.dumps({
        'success': False,
        'error': 'Method not allowed'
    }), status=405)

def serve_file(request, filename):
    file_path = os.path.join(settings.BASE_DIR, 'downloads', filename)
    
    if not os.path.exists(file_path):
        raise Http404("File not found")
    
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='audio/mpeg')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
