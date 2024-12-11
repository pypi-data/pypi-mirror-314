from celery import current_app as app

from zs_utils.base_support import services


@app.task(queue="low")
def close_inactive_tickets_task(**kwargs):
    """
    Закрытие всех неактивных обращений в поддержку для всех пользователей
    """
    services.CommonSupportTicketService.close_inactive_tickets()
