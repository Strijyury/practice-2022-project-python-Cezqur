from decimal import Decimal

from django.db.models import QuerySet, Sum, Q, DecimalField
from django.db.models.functions import Coalesce

from ...constants import TransactionTypes


class TransactionQuerySet(QuerySet):
    def aggregate_totals(self) -> dict[str, Decimal]:
        return self.aggregate(
            total_income=Coalesce(
                Sum(
                    'amount',
                    filter=Q(transaction_type=TransactionTypes.INCOME),
                ),
                0,
                output_field=DecimalField(),
            ),
            total_expenses=Coalesce(
                Sum(
                    'amount',
                    filter=Q(transaction_type=TransactionTypes.EXPENSE),
                ),
                0,
                output_field=DecimalField(),
            ),
        )

    def get_balance(self):
        aggregated_queryset = self.aggregate_totals()
        total_income = aggregated_queryset.get('total_income')
        total_expenses = aggregated_queryset.get('total_expenses')
        balance = total_income - total_expenses

        return balance
