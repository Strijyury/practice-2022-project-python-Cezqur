from typing import Type

from django.db.models import QuerySet
from rest_framework import viewsets, serializers, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from django_filters import rest_framework as filters

from ..filters import TransactionCategoryFilter
from ..models import TransactionCategory
from ..serializers import (
    TransactionCategorySerializer,
    TransactionCategoryTransactionSumSerializer,
)


class TransactionCategoryViewSet(mixins.CreateModelMixin,
                                 mixins.ListModelMixin,
                                 viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TransactionCategoryFilter

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        serializer_class = TransactionCategorySerializer

        if self.action == 'transactions_by_categories':
            serializer_class = TransactionCategoryTransactionSumSerializer

        return serializer_class

    def get_queryset(self) -> QuerySet:
        if self.action == 'transactions_by_categories':
            queryset = TransactionCategory.objects.filter(
                transactions__user=self.request.user
            ).annotate_with_transaction_sums()
        elif self.action == 'diagram':
            queryset = TransactionCategory.objects.filter(transactions__user=self.request.user)
        else:
            queryset = TransactionCategory.objects.annotate_with_transaction_sums()

        return queryset

    @action(methods=('GET',), detail=False, url_path='transactions-by-categories')
    def transactions_by_categories(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @action(methods=('GET',), detail=False, url_path='diagram')
    def diagram(self, request):
        q = self.get_queryset().get_diagram()
        return Response(list(q))
