from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'check-budget-limits': {
        'task': 'core.tasks.check_budget_limits',
        'schedule': crontab(hour=0, minute=0),  # Run daily at midnight
    },
    'update-financial-goals': {
        'task': 'core.tasks.update_financial_goals',
        'schedule': crontab(hour='*/6'),  # Run every 6 hours
    },
    'generate-monthly-reports': {
        'task': 'core.tasks.generate_monthly_report',
        'schedule': crontab(0, 0, day_of_month='1'),  # Run on the 1st of each month
    },
}
