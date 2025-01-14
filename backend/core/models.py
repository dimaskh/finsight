from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=5)
    
    class Meta:
        verbose_name_plural = 'currencies'
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    icon = models.CharField(max_length=50, blank=True)  # Font Awesome icon name
    is_expense = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'categories'
        unique_together = ['name', 'user']
    
    def __str__(self):
        return self.name

class Account(models.Model):
    ACCOUNT_TYPES = [
        ('CASH', 'Cash'),
        ('BANK', 'Bank Account'),
        ('CREDIT', 'Credit Card'),
        ('INVESTMENT', 'Investment Account'),
        ('SAVINGS', 'Savings Account'),
    ]
    
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    initial_balance = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    current_balance = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=Decimal('0.00')
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_account_type_display()})"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('EXPENSE', 'Expense'),
        ('INCOME', 'Income'),
        ('TRANSFER', 'Transfer'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    to_account = models.ForeignKey(
        Account, 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE,
        related_name='incoming_transfers'
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.date} - {self.amount} - {self.category}"

class Budget(models.Model):
    PERIOD_CHOICES = [
        ('MONTHLY', 'Monthly'),
        ('YEARLY', 'Yearly'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.category} - {self.amount} {self.currency.code} ({self.period})"

class FinancialGoal(models.Model):
    GOAL_TYPES = [
        ('SAVINGS', 'Savings Target'),
        ('DEBT', 'Debt Repayment'),
        ('INVESTMENT', 'Investment Target'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES)
    target_amount = models.DecimalField(max_digits=15, decimal_places=2)
    current_amount = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    target_date = models.DateField()
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.target_amount} {self.currency.code}"
