import os
import smtplib
import redis
import logging

from email.mime.text import MIMEText
from threading import Thread

from django.core.cache import cache
from django.http import HttpResponseRedirect

from post.models import User, Article

logger = logging.getLogger('inf')

rds = redis.Redis()

def send_email(user_id):
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.163.com'
    MAIL_PORT = 25       # TLS协议对应端口号是25
    # MAIL_USE_TLS = True  # 使用TLS协议
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '18600218950@163.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or '19880404h'
    SERVER_IP = os.environ.get('SERVER_IP') or '10.0.129.64'

    user = User.objects.filter(id=user_id).first()
    token = user.generate_activate_token().decode('utf-8')
    content = 'http://%s:8000/active/?token=%s' % (SERVER_IP, token)
    # print(content)
    message = MIMEText(content)
    message['Subject'] = '账户激活'
    message['From'] = MAIL_USERNAME

    mail_server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
    mail_server.login(MAIL_USERNAME, MAIL_PASSWORD)
    mail_server.sendmail(MAIL_USERNAME, ['%s'%user.email], message.as_string())
    mail_server.quit()


def async_send_email(user_id):
    thread = Thread(target=send_email, args=[user_id,])
    thread.start()
    return thread


def get_user(request):
    username = request.session.get('username', None)
    if username:
        user = User.objects.filter(username=username).first()
    else:
        user = None
    return user


def login_required(view_func):
    def wrap(request, *args, **kwargs):
        if get_user(request):
            return view_func(request, *args, **kwargs)
        else:
            next = request.path
            return HttpResponseRedirect('/login/?next=%s' % next)
    return wrap


def page_cache(timeout):
    def wrap1(view_func):
        def wrap2(request, *args, **kwargs):
            key = 'page-%s' % request.get_full_path()
            response = cache.get_or_set(key, None)
            if response is None:
                response = view_func(request, *args, **kwargs)
                cache.set(key, response, timeout)
                # print('缓存 %s cache set' % key)
            return response
        return wrap2
    return wrap1


def cache_count(view_func):
    def wrap(request, *args, **kwargs):
        # ip = request.META['REMOTE_ADDR']
        article_id = int(request.GET.get('article_id', 1))
        # logger.info('%s %s' % (ip, article_id))
        rds.zincrby('counter', article_id)
        return view_func(request, *args, **kwargs)
    return wrap


def get_top10():
    top_members = rds.zrevrange('counter', 0, 9, withscores=True)
    article_idlist = [(int(article_id), int(count)) for article_id, count in top_members]
    article_list = [(Article.objects.filter(id=article_id).first(), count) for article_id, count in article_idlist]
    return article_list
