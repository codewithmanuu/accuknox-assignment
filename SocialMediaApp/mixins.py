import uuid
import re
from django.contrib.auth.models import User
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

def create_user_name():
    slug = uuid.uuid4()
    if User.objects.filter(username=slug).exists():
        return create_user_name()
    else:
        return slug
    
def has_digit(input_string):
    pattern = r'^[a-zA-Z]+$'

    if re.match(pattern, input_string):
        return False
    else:
        return True

class ObjectPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response(data)
    
class CustomUserRateThrottle(UserRateThrottle):
    rate = '3/minute'

    def allow_request(self, request, view):
        allowed = super().allow_request(request, view)
        return allowed
