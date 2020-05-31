from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaulttags import register
from .forms import EmailPostForm
from .models import Post, Comment
from .forms import Post_form, Comment_form
from django.core.mail import send_mail


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


month_dict = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь"
}


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    posts_five = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[0:4]
    dict_comm = {}
    for post in posts:
        n = Comment.objects.filter(page=post.pk).count()
        dict_comm[post.pk] = n

    paginator = Paginator(posts, 4)  # 4 поста на каждой странице
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        posts = paginator.page(paginator.num_pages)

    context = {

        "title": "Страница блога",
        "posts": posts,
        "posts_five": posts_five,
        "arh": month_dict,
        "page": page,
        "dict_comm": dict_comm
    }
    return render(request, 'blog/post_list.html', context=context)


def index(request):
    print(request.GET)
    name = request.GET.get('name')
    type = request.GET.get('type')
    humanoid = request.GET.get('humanoid')
    # print(name)
    # return HttpResponse('Hello, Ernest')
    if humanoid == "ДА":
        s_hum = 'ты человечище!'
    else:
        s_hum = 'жаль, что ты не человек!'

    return HttpResponse('<h> Привет, %s %s,- %s </h>' % (type, name, s_hum))


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
    comments = Comment.objects.filter(page=pk)
    title = "Статья"
    context = {
        'post': post,
        'posts_five': posts_five,
        'title': title,
        'comments': comments,
        "arh": month_dict
    }

    return render(request, 'blog/post_detail.html', context=context)


def arhive_month(request, year, month):
    posts = Post.objects.filter(published_date__month=month).filter(published_date__year=year).order_by(
        '-published_date')
    title = "Архив" + " " + month_dict[month] + " " + str(year)
    return render(request, 'blog/arhive_month.html', {'posts': posts, 'title': title})


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

    context = {
        'form': form,
        'title': 'new post'
    }

    return render(request, 'blog/post_edit.html', context=context)


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = Post_form(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.update_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = Post_form(instance=post)
    context = {
        'form': form,
        'title': 'edit post'
    }

    return render(request, 'blog/post_edit.html', context=context)


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
    context = {
        'form': form,
        'title': 'new comment'
    }

    return render(request, 'blog/comment_edit.html', context=context)


def about_me(request):
    context = {
        'title': 'about'
    }

    return render(request, 'blog/about_me.html', context=context)


def contact(request):
    sent = False
    if request.method == 'POST':
        # Форма была отправлена
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля формы прошли проверку
            cd = form.cleaned_data

            subject = 'mail from {} fo SergeyZhigar, back email:{}'.format(cd['name'], cd['email'])
            message = '{} wants to ask: {}'.format(cd['name'], cd['question'])
            send_mail(subject, message, 'zhyhar.siarhei@gmail.com', ['zhyhar.siarhei@gmail.com', cd['email']])
            sent = True
    else:
        form = EmailPostForm()
    context = {
        'form': form,
        'sent': sent
    }
    return render(request, 'blog/contact.html', context=context)


def post_share(request, pk):
    # Получить пост по id
    post = get_object_or_404(Post, pk=pk)
    sent = False
    if request.method == 'POST':
        # Форма была отправлена
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля формы прошли проверку
            cd = form.cleaned_data
            post_url = request.build_absolute_uri('/post/{}/'.format(post.pk))
            subject = '{} ({}) recommends you reading " {}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s question: {}'.format(post.title, post_url, cd['name'], cd['question'])
            send_mail(subject, message, 'zhyhar.siarhei@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    context = {
        'post': post,
        'form': form,
        'sent': sent
    }
    return render(request, 'blog/share.html', context=context)
