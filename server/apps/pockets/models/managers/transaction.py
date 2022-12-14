from decimal import Decimal

from django.db.models import Manager

from ..querysets import TransactionQuerySet


class TransactionManager(Manager):
    def get_queryset(self, **kwargs) -> TransactionQuerySet:
        return TransactionQuerySet(
            self.model,
            using=self._db,
        )

    def annotate_with_transaction_sums(self) -> dict[str, Decimal]:
        return self.get_queryset().aggregate_totals()

    def get_balance(self):
        return self.get_queryset().get_balance()
