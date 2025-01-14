from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Transaction, Account

@receiver(pre_save, sender=Transaction)
def update_account_balance_on_transaction_change(sender, instance, **kwargs):
    """
    Update account balances when a transaction is modified.
    For new transactions, the old_instance won't exist.
    """
    try:
        old_instance = Transaction.objects.get(pk=instance.pk)
        # Revert the old transaction's effect
        if old_instance.transaction_type in ['EXPENSE', 'TRANSFER']:
            old_instance.account.current_balance += old_instance.amount
            old_instance.account.save()
        elif old_instance.transaction_type == 'INCOME':
            old_instance.account.current_balance -= old_instance.amount
            old_instance.account.save()
            
        if old_instance.transaction_type == 'TRANSFER' and old_instance.to_account:
            old_instance.to_account.current_balance -= old_instance.amount
            old_instance.to_account.save()
            
    except Transaction.DoesNotExist:
        pass  # This is a new transaction

@receiver(post_save, sender=Transaction)
def update_account_balance_on_transaction_save(sender, instance, created, **kwargs):
    """
    Update account balances when a transaction is created or updated.
    """
    if instance.transaction_type in ['EXPENSE', 'TRANSFER']:
        instance.account.current_balance -= instance.amount
        instance.account.save()
    elif instance.transaction_type == 'INCOME':
        instance.account.current_balance += instance.amount
        instance.account.save()
        
    if instance.transaction_type == 'TRANSFER' and instance.to_account:
        instance.to_account.current_balance += instance.amount
        instance.to_account.save()

@receiver(post_save, sender=Account)
def initialize_account_balance(sender, instance, created, **kwargs):
    """
    Set the current balance to initial balance when a new account is created.
    """
    if created and instance.initial_balance != instance.current_balance:
        instance.current_balance = instance.initial_balance
        instance.save()
