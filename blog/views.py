from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.utils import timezone

month_dict = {
    1:"Январь",
    2:"Февраль",
    3:"Март",
    4:"Апрель",
    5:"Май",
    6:"Июнь",
    7:"Июль",
    8:"Август",
    9:"Сентябрь",
    10:"Октябрь",
    11:"Ноябрь",
    12:"Декабрь"
}

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    posts_five = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[0:4]

    context={

        "title":"Страница блога",
        "posts": posts,
        "posts_five" : posts_five,
        "arh": month_dict
    }
    return render(request, 'blog/post_list.html', context=context)

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

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    posts_five = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[0:4]
    title = "Статья"
    return render(request, 'blog/post_detail.html', {'post': post,'posts_five':posts_five,'title': title})

def arhive_month(request, year, month):
    posts = Post.objects.filter(published_date__month=month).filter(published_date__year=year).order_by('-published_date')
    title = "Архив" + " " + month_dict[month]+" "+str(year)
    return render(request, 'blog/arhive_month.html', {'posts': posts,'title': title})