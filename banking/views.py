from django.db.models import Q
from rest_framework import viewsets, permissions
from .models import Credit, Deposit, Transaction
from .serializers import CreditSerializer, DepositSeriallizer, TransactionSeriallizer

class CreditViewSet(viewsets.ModelViewSet):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Credit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DepositViewSet(viewsets.ModelViewSet):
    queryset = Credit.objects.all()
    serializer_class = DepositSeriallizer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Deposit.objects.filter(user = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Credit.objects.all()
    serializer_class = TransactionSeriallizer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.object.filter(
            Q(credit_user = self.request.user) |
            Q(deposit_user = self.request.user)
        )
    
    