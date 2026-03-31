from rest_framework.pagination import PageNumberPagination
from django.conf import settings


class DefaultPageNumberPagination(PageNumberPagination):
    page_size = settings.PRODUCTS_PER_PAGE
    page_size_query_param = "page_size"
