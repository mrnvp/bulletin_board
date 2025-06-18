from django_filters import FilterSet, CharFilter
from .models import Reply

class ReplyFilter(FilterSet):
    post_title = CharFilter(field_name = 'post__title', lookup_expr='icontains', label = 'Поиск по заголовку объявления')
    class Meta:
        model = Reply
        fields = []