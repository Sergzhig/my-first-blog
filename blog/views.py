from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.utils import timezone


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')git
    return render(request, 'blog/post_list.html', {'posts' : posts})

def index(request):
    print(request.GET)
    name=request.GET.get('name')
    type = request.GET.get('type')
    humanoid = request.GET.get('humanoid')
    #print(name)
    #return HttpResponse('Hello, Ernest')
    if humanoid =="ДА":
        s_hum='ты человечище!'
    else:
        s_hum='жаль, что ты не человек!'

    return HttpResponse('<h> Привет, %s %s,- %s </h>'%(type,name,s_hum))

def index_ren(request):
    name = request.GET.get('name')
    type = request.GET.get('type')
    name_length = len(name)
    context = {
        "name": name,
        "name_length": name_length,
        "type": type
    }
    return render(request, 'index.html', context=context)