from django_filters import rest_framework as filters
from django_filters.filters import OrderingFilter


class TransactionFilter(filters.FilterSet):
    date__month = filters.NumberFilter(field_name='transaction_date__month',
                                       lookup_expr='exact',
                                       label='Месяц')
    date__year = filters.NumberFilter(field_name='transaction_date__year',
                                      lookup_expr='exact',
                                      label='Год')
    ordering = OrderingFilter(
        fields=(
            ('transaction_date', 'Дата'),
            ('category__name', 'Категория'),
            ('amount', 'Сумма'),
        )
    )


class TransactionCategoryFilter(filters.FilterSet):
    date__month = filters.NumberFilter(field_name='transactions__transaction_date__month',
                                       method='month_filter',
                                       label='Месяц')

    def month_filter(self, queryset, name, value):
        return queryset.annotate_with_transaction_sums(month=value)
