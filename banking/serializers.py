from rest_framework import serializers
from .models import Credit, Deposit, Transaction

class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = '__all__'
        read_only_fields = ('user', 'issued_at')

class DepositSeriallizer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = '__all__'
        read_only_fields = ('user', 'opened_at')

class TransactionSeriallizer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('created_at',)

    def validate(self, attrs):
        credit = attrs.get('credit')
        deposit = attrs.get('deposit')

        if (credit is None) == (deposit is None):
            raise serializers.ValidationError('Транзакция должна быть привязана ровно к одному: кредиту ИЛИ вкладу')

        request = self.context.get('request')
        if request and request.user:
            if credit and credit.user != request.user:
                raise serializers.ValidationError({'credit': 'Нельзя создать транзакцию на чужой кредит'})
            if deposit and deposit.user != request.user:
                raise serializers.ValidationError({'deposit': 'Нельзя создать транзакцию на чужой вклад'})

        return attrs