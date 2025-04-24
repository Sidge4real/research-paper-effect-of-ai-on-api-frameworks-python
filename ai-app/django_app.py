from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.paginator import Paginator
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import json
from bson import ObjectId
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

try:
    # MongoDB connection using environment variable
    client = MongoClient(os.getenv('MONGODB_URI'))
    # Test the connection
    client.admin.command('ping')
    db = client.researchDB.django
except ConnectionFailure:
    print("Failed to connect to MongoDB. Please check your connection string and network connection.")
    raise

def get_posts(request):
    page = int(request.GET.get('page', 1))
    posts_list = list(db.find())
    paginator = Paginator(posts_list, 10)
    posts = paginator.get_page(page)
    
    # Convert ObjectId to string for JSON serialization
    serialized_posts = []
    for post in posts:
        post['_id'] = str(post['_id'])
        serialized_posts.append(post)
    
    return JsonResponse(serialized_posts, safe=False)

def get_post(request, id):
    try:
        post = db.find_one({'_id': ObjectId(id)})
        if post:
            post['_id'] = str(post['_id'])
            return JsonResponse(post)
        return JsonResponse({'error': 'Post not found'}, status=404)
    except:
        return JsonResponse({'error': 'Invalid ID'}, status=400)

@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            result = db.insert_one(data)
            return JsonResponse({'_id': str(result.inserted_id)}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


summarizer = pipeline("summarization",
                    model="facebook/bart-large-cnn",
                    torch_dtype=torch.float16)

@csrf_exempt
def summarize(request):
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            text = data.get('text', '')
            
            if not text:
                return JsonResponse({'error': 'No text provided'}, status=400)
            
            summary = summarizer(text,
                               max_length=150,
                               min_length=40,
                               do_sample=False)
            
            return JsonResponse({'summary': summary[0]['summary_text']})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)