from collections import OrderedDict

from rest_framework import serializers

from ..constants import TransactionErrors, TransactionTypes
from ..models import Transaction, TransactionCategory
from .transaction_category import TransactionCategorySerializer


class TransactionRetrieveSerializer(serializers.ModelSerializer):
    category = TransactionCategorySerializer()

    class Meta:
        model = Transaction
        fields = ('id', 'category', 'transaction_date', 'amount', 'transaction_type')


class TransactionCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=TransactionCategory.objects.all(),
                                                  required=False)
    transaction_type = serializers.ChoiceField(choices=TransactionTypes.CHOICES)

    class Meta:
        model = Transaction
        fields = ('id', 'category', 'transaction_type', 'transaction_date', 'amount')

    def validate(self, data):
        if data['transaction_type'] == TransactionTypes.INCOME and data.get('category'):
            raise serializers.ValidationError(TransactionErrors.CATEGORY_NOT_ALLOWED)
        elif data['transaction_type'] == TransactionTypes.EXPENSE and not data.get('category'):
            raise serializers.ValidationError(TransactionErrors.CATEGORY_IS_REQUIRE)
        else:
            return data

    def create(self, validated_data: dict) -> Transaction:
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    @property
    def data(self) -> OrderedDict:
        """
        Сделано для того, чтобы при создании объекта можно было передвавть id категории, а после
        создания поле категории возвращалось как объект
        """
        return TransactionRetrieveSerializer(instance=self.instance).data


class TransactionGlobalSerializer(serializers.Serializer):
    total_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)


class TransactionExpensesByCategorySerializer(serializers.ModelSerializer):
    category = TransactionCategorySerializer()

    class Meta:
        model = Transaction
        fields = ('id', 'category', 'transaction_date', 'transaction_type', 'amount')


class TransactionBalanceSerializer(serializers.Serializer):
    balance = serializers.SerializerMethodField()

    def get_balance(self, obj):
        return obj
