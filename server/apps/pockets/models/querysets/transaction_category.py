from django.db.models import QuerySet, Sum, Q, DecimalField
from django.db.models.functions import Coalesce


class TransactionCategoryQuerySet(QuerySet):
    def annotate_with_transaction_sums(self, month=None):
        """
        :return: TransactionCategoryQuerySet
        """

        filter_dict = {}
        if month:
            filter_dict['transactions__transaction_date__month'] = month

        return self.annotate(
            transactions_sum=Coalesce(
                Sum('transactions__amount',
                    filter=Q(**filter_dict)),
                0,
                output_field=DecimalField(),
            ),
        ).order_by('-transactions_sum', 'name')

    def get_diagram(self):
        annotated_queryset = self.annotate_with_transaction_sums()
        top_three_category_queryset = annotated_queryset.values_list('name', 'transactions_sum')[:3]
        other_categories = annotated_queryset.exclude(
                pk__in=top_three_category_queryset.values_list('pk', flat=True)
            ).aggregate(
                Другое=Coalesce(
                    Sum('transactions__amount'),
                    0,
                    output_field=DecimalField(),
                )
            )
        top_three_category_queryset_list = [i for i in top_three_category_queryset]
        other_categories_list = [(k, v) for k, v in other_categories.items()]
        top_three_category_queryset_list.extend(other_categories_list)

        return top_three_category_queryset_list
