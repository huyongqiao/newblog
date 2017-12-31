from django.core.cache import cache
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

from post.logic import get_user


class Record_Online_User(MiddlewareMixin):
    def process_request(self, request):
        ip = request.META['REMOTE_ADDR']
        user = get_user(request)
        pass
