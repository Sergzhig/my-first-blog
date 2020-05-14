from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Post, Comment
from .forms import Post_form, Comment_form
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
    comments =Comment.objects.filter(page=pk)
    title = "Статья"
    context = {
        'post': post,
        'posts_five':posts_five,
        'title': title,
        'comments':comments,
        "arh": month_dict
    }

    return render(request, 'blog/post_detail.html', context=context)

def arhive_month(request, year, month):
    posts = Post.objects.filter(published_date__month=month).filter(published_date__year=year).order_by('-published_date')
    title = "Архив" + " " + month_dict[month]+" "+str(year)
    return render(request, 'blog/arhive_month.html', {'posts': posts,'title': title})

def post_new(request):
    if request.method == "POST":
        form = Post_form(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = Post_form()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = Post_form(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.update_date=timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = Post_form(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def comment_new(request):
    if request.method == "POST":
        form = Comment_form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.published_date = timezone.now()
            comment.save()
            return redirect('post_detail', pk=comment.page_id)
    else:
        form = Comment_form()
    return render(request, 'blog/comment_edit.html', {'form': form})


