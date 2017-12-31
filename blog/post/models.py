import hashlib
import json

from django.db import models
from django.core import serializers
from django.db import models
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from blog.settings import SECRET_KEY

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    password_hash = models.CharField(max_length=128)
    email = models.CharField(max_length=32)
    create_time = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)
    # image = models.ImageField(upload_to='images', verbose_name='文件缩略图')
    icon = models.CharField(max_length=20, default='default.png')
    friend_id = models.IntegerField(default=0)


    class Meta:
        db_table = 'user'

    @property
    def password(self):
        return AttributeError('密码不可取')

    @password.setter
    def password(self, password):
        password_hash = hashlib.sha1(password.encode('utf-8')).hexdigest()
        self.password_hash = password_hash

    def verify_password(self, password):
        password_hash = hashlib.sha1(password.encode('utf-8')).hexdigest()
        if password_hash == self.password_hash:
            return True
        else:
            return False

    def generate_activate_token(self, expires_in=3600):
        s = Serializer(SECRET_KEY, expires_in=expires_in)
        return s.dumps({'id': self.id})

    @staticmethod
    def check_activate_token(token):
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except:
            return False
        user = User.objects.filter(id=data['id']).first()
        if user is None:
            return False
        if not user.confirmed:
            # 没有激活就激活
            user.confirmed = True
            user.save()
        return True


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    read_count = models.IntegerField(default=0)
    tag = models.CharField(max_length=50)
    comment_count = models.IntegerField(default=0)
    class Meta:
        db_table = 'article'



class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    article_id = models.IntegerField(default=0)
    class Meta:
        db_table = 'comment'


class Collect(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    article_id = models.IntegerField()
    class Meta:
        db_table = 'collect'


class Friend(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    friend_id = models.IntegerField()

