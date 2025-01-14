from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal

from .models import Budget, Transaction, FinancialGoal

@shared_task
def check_budget_limits():
    """
    Daily task to check if any budget categories are close to or exceeding their limits
    """
    current_date = timezone.now()
    budgets = Budget.objects.filter(is_active=True)
    
    for budget in budgets:
        # Calculate total spending for this budget's category this month
        total_spent = Transaction.objects.filter(
            category=budget.category,
            date__month=current_date.month,
            date__year=current_date.year
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
        
        # Alert if spending is over 80% of budget
        if total_spent >= (budget.amount * Decimal('0.8')):
            send_budget_alert.delay(
                budget.id,
                total_spent,
                budget.amount
            )

@shared_task
def send_budget_alert(budget_id, spent_amount, budget_amount):
    """
    Send email alert for budget limits
    """
    budget = Budget.objects.get(id=budget_id)
    percentage = (spent_amount / budget_amount) * 100
    
    send_mail(
        subject=f'Budget Alert: {budget.category.name}',
        message=f'You have spent {percentage:.1f}% ({spent_amount} {budget.currency.code}) '
                f'of your {budget.category.name} budget ({budget_amount} {budget.currency.code})',
        from_email='notifications@finsight.com',
        recipient_list=[budget.user.email],
    )

@shared_task
def generate_monthly_report(user_id):
    """
    Generate monthly financial report for user
    """
    # Implementation for generating complex financial reports
    # This could be CPU-intensive, involving many calculations
    pass

@shared_task
def process_bank_statement_import(file_path, account_id):
    """
    Process imported bank statement files
    """
    # Implementation for parsing and importing bank statements
    # This could be time-consuming for large files
    pass

@shared_task
def update_financial_goals():
    """
    Update progress on financial goals
    """
    goals = FinancialGoal.objects.filter(is_completed=False)
    for goal in goals:
        # Calculate current progress
        # Send notifications if milestones are reached
        pass
