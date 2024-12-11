from celery import current_app as app

from zs_utils.websocket import services


@app.task()
def send_user_message_to_websocket_task(user_id: int, event_type: str, data: dict, **kwargs) -> None:
    services.WebsocketService.send_data_to_user(
        user_id=user_id,
        content={
            "event_type": event_type,
            "data": data,
        },
    )


@app.task()
def send_notification_group_message_to_websocket_task(
    user_id: int,
    notification: str,
    data: dict,
    **kwargs,
) -> None:
    services.WebsocketService.send_data_to_notification_group(
        user_id=user_id,
        notification=notification,
        data=data,
    )
