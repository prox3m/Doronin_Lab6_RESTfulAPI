from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

class Credit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credits') #related_name для читабельности запросов
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_months = models.PositiveIntegerField()
    issued_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-issued_at']

    def __str__(self):
        return f'Credit #{self.pk} - {self.amount} ({self.user.username})'

class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deposits')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_months = models.PositiveIntegerField()
    opened_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-opened_at']

    def __str__(self):
        return f'Deposit #{self.pk} - {self.amount} ({self.user.username})'

class Transaction(models.Model):
    TYPE_CHOICES = [
        ('payment', 'Платеж по кредиту'),
        ('interest', 'Начисление процентов'),
        ('withdrawal', 'Снятие/выплата'),
    ]

    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, null=True, blank=True, related_name='transactions')
    deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE, null=True, blank=True, related_name='transactions')

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(credit__isnull=False, deposit__isnull=True) | #| XOR
                    Q(credit__isnull=True, deposit__isnull=False)
                ),
                name='transaction_exactly_one_target',
            ),
        ]

    def __str__(self):
        target = self.credit or self.deposit
        return f'Transaction #{self.pk} - {self.type} {self.amount}'