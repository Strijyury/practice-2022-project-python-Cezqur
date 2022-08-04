from django.db.models import Manager

from ..querysets import TransactionCategoryQuerySet


class TransactionCategoryManager(Manager):
    def get_queryset(self, **kwargs) -> TransactionCategoryQuerySet:
        return TransactionCategoryQuerySet(self.model, using=self._db)

    def annotate_with_transaction_sums(self, month=None) -> 'TransactionCategoryQuerySet':
        return self.get_queryset().annotate_with_transaction_sums(month)

    def get_diagram(self):
        return self.get_queryset().get_diagram()
