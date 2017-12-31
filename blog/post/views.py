import os

from PIL import Image
from django.contrib import messages
from django.contrib.messages import add_message
from django.core.cache import cache
from django.core.files.base import ContentFile
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from blog.settings import MEDIA_ROOT
from post.forms import RegisterForm
from post.logic import async_send_email, page_cache, cache_count, get_top10, get_user, login_required
from post.models import User, Article, Comment, Collect


def home(request):
    articles = Article.objects.all()
    top10 = get_top10()
    context = {'articles': articles, 'current_user': get_user(request), 'top10': top10}
    return render(request, 'home.html', context)


def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            password2 = form.cleaned_data.get('password2')

            if password == password2:
                user = User()
                user.username = username
                user.email = email
                user.password = password
                user.save()

                async_send_email(user.id)

                message = '恭喜%s，账号已经注册成功，请尽快去%s邮箱激活账号' % (username, email)
                add_message(request, messages.INFO, message)

                return HttpResponseRedirect('/login/')
            else:
                add_message(request, messages.INFO, '两次密码不一致，请重新输入')
                return HttpResponseRedirect('/register/')

    return render(request, 'register.html', {'form': form})

def check_user(request):
    pre_username  = request.GET.get('username')
    if len(User.objects.filter(username=pre_username)) == 0:
        context = {'status':'用户名可用'}
    else:
        context = {'status': '用户名已被使用'}

    return JsonResponse(context)


def active(request):
    token = request.GET.get('token')
    if User.check_activate_token(token):
        add_message(request, messages.INFO, '账号激活成功，请登录')
        return HttpResponseRedirect('/login/')
    else:
        add_message(request, messages.INFO, '账号激活失败，请重新注册')
        return HttpResponseRedirect('/register/')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next_url')

        # 如果用户名和密码都正确，返回user对象，否则返回None
        if len(User.objects.filter(username=username)) == 0:
            add_message(request, messages.INFO, '账号错误')

        else:
            user = User.objects.filter(username=username).first()
            if user.verify_password(password):
                if user.confirmed:
                    request.session['username'] = username
                    response = HttpResponseRedirect(next_url)
                    add_message(request, messages.INFO, '登录成功')
                    return response
                else:
                    add_message(request, messages.INFO, '此账号未激活，请尽快去注册邮箱激活！')
            else:
                add_message(request, messages.INFO, '密码错误')
                return HttpResponseRedirect('/login/?next=%s' % next_url)

        return HttpResponseRedirect('/login/?next=%s' % next_url)

    next_url = request.GET.get('next', '/')
    context = {'next_url': next_url}
    return render(request, 'login.html', context)


@login_required
def logout(request):
    del request.session['username']
    add_message(request, messages.INFO, '成功退出')
    return HttpResponseRedirect('/')


@login_required
def user_info(request):
    user = get_user(request)
    context = {'current_user': user}
    return render(request, 'user_info.html', context)


@login_required
def post(request):
    if request.method == 'POST':
        user = get_user(request)
        article = Article()
        article.title = request.POST.get('title')
        article.author = user.username
        article.content = request.POST.get('content')
        article.save()

        add_message(request, messages.INFO, '帖子发表成功')
        return HttpResponseRedirect('/')

    context = {'current_user': get_user(request)}
    return render(request, 'post.html', context)

# 使用page_cache缓存，article在缓存中操作，收藏和阅读量会出Bug，刷新不及时
# @page_cache(timeout=30)
@cache_count
def detail(request):
    # print('数据库', request.get_full_path())

    user = get_user(request)
    article_id = request.GET.get('article_id')
    article = Article.objects.filter(id=article_id).first()
    article.read_count += 1
    article.save()

    comments = Comment.objects.filter(article_id=article_id)
    current_path = request.get_full_path()

    if user and len(Collect.objects.filter(Q(user_id=user.id) & Q(article_id=article_id))):
        collect_flag = True
    else:
        collect_flag = False

    context = {'article': article, 'comments': comments, 'current_path': current_path,
               'current_user': get_user(request), 'collect_flag': collect_flag}
    return render(request, 'detail.html', context)


@login_required
def comment(request):
    user = get_user(request)
    article_id = request.POST.get('article_id')

    comment = Comment()
    comment.article_id = article_id
    comment.author = user.username
    comment.content = request.POST.get('content')
    comment.save()

    article = Article.objects.filter(id=article_id).first()
    article.comment_count += 1
    article.save()

    message = '评论成功'
    add_message(request, messages.INFO, message)

    current_path = request.POST.get('current_path')
    return HttpResponseRedirect(current_path)


@login_required
def my_articles(request):
    user = get_user(request)
    articles = Article.objects.filter(author=user.username)
    context =  {'current_user': user, 'articles': articles}
    return render(request, 'my_articles.html', context)


@login_required
def delete_article(request):
    article_id = request.GET.get('article_id')
    Article.objects.filter(id=article_id).first().delete()
    add_message(request, messages.INFO, '删除帖子成功')
    return HttpResponseRedirect('/my_articles/')


def search(request):
    keyword = request.GET.get('keyword')
    articles = Article.objects.filter(Q(title__contains=keyword) | Q(content__contains=keyword))
    context = {'articles': articles}
    return render(request, 'search_result.html', context)


@login_required
def add_collect(request):
    user = get_user(request)
    article_id = request.GET.get('article_id')

    collect = Collect()
    collect.user_id = user.id
    collect.article_id = article_id
    collect.save()

    add_message(request, messages.INFO, '收藏成功')
    return HttpResponseRedirect('/my_collect/')


@login_required
def del_collect(request):
    user = get_user(request)
    article_id = request.GET.get('article_id')

    collect = Collect.objects.filter(Q(user_id=user.id) & Q(article_id=article_id)).first()
    collect.delete()

    add_message(request, messages.INFO, '删除成功')
    return HttpResponseRedirect('/my_collect/')


@login_required
def my_collect(request):
    user = get_user(request)
    collects = Collect.objects.filter(user_id=user.id).all()
    article_idlist = [collect.article_id for collect in collects]
    articles = Article.objects.filter(id__in=article_idlist).all()
    context = {'current_user': user, 'articles': articles}
    return render(request, 'my_collect.html', context)


@login_required
def upload_icon(request):
    user = get_user(request)
    if request.method == 'POST':
        f = request.FILES['icon']  #request.FILES为类字典结构
        file_ext = os.path.splitext(f.name)[-1]

        if  file_ext not in ['.png','.jpg']:
            add_message(request, messages.INFO, '只能上传png/jpg格式图片，请重新上传！')
            return HttpResponseRedirect('/upload_icon/')

        icon_name = user.username + file_ext
        icon_path = os.path.join(MEDIA_ROOT, icon_name)  #接收端的文件路径

        with open(icon_path, 'wb') as icon:
            for part in f.chunks():  #分包发送，分包接收，分包写入，收到一段写入一段
                icon.write(part)
                icon.flush() #刷新缓冲区，防止数据拥堵

        try:
            img = Image.open(icon_path)  #打开上传文件
        except OSError:
            os.remove(os.path.join(MEDIA_ROOT, icon_path))  #无效删除
            add_message(request, messages.INFO, '上传文件并非图片，请重新上传！')
            return HttpResponseRedirect('/upload_icon/')

        img.thumbnail((64,64))       #把原来的文件压缩成64*64的缩略图
        img.save(icon_path)          #保存缩略图文件，替代用户上传的图片

        if user.icon != 'default.png' and user.icon != icon_name:  #删除用户原来的头像文件，使用默认头像的不能删除
            os.remove(os.path.join(MEDIA_ROOT, user.icon))

        user.icon = icon_name
        user.save()

        add_message(request, messages.INFO, '头像修改成功')
        return HttpResponseRedirect('/user_info/')

    return render(request, 'upload_icon.html', {'current_user': user})


