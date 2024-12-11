from datetime import datetime, timedelta

from zs_utils.api.ebay.base_api import EbayTradingAPI
from zs_utils.api.ebay.data.enums import PlatformNotificationEventTypeEnum


__all__ = [
    "GetNotificationSettings",
    "GetAppNotificationSettings",
    "GetUserNotificationSettings",
    "GetNotificationsUsage",
    "SetNotificationSettings",
    "ReviseNotifications",
    "SubscribeNotification",
    "UnSubscribeNotification",
]


class GetNotificationSettings(EbayTradingAPI):
    """
    Docs:
    https://developer.ebay.com/Devzone/XML/docs/Reference/eBay/GetNotificationPreferences.html
    """

    method_name = "GetNotificationPreferences"

    def get_params(self, preference_level: str, **kwargs):
        assert preference_level in [
            "Application",
            "Event",
            "User",
            "UserData",
        ], f'Недопустимое значение "preference_level": {preference_level}'
        return {
            "PreferenceLevel": preference_level,
            "OutputSelector": None,
        }

    # DEPRECATED
    # def make_request(self, **kwargs):
    #     is_success, message, objects = super().make_request(**kwargs)
    #     if objects.get("errors", []):
    #         if objects["errors"][0].get("ErrorCode", None) == "12209":
    #             is_success = True
    #             objects["results"] = []
    #     return is_success, message, objects


class GetAppNotificationSettings(GetNotificationSettings):
    def get_params(self, **kwargs):
        kwargs["preference_level"] = "Application"
        return super().get_params(**kwargs)


class GetUserNotificationSettings(GetNotificationSettings):
    def get_params(self, **kwargs):
        kwargs["preference_level"] = "User"
        return super().get_params(**kwargs)


class GetNotificationsUsage(EbayTradingAPI):
    """
    Docs:
    https://developer.ebay.com/Devzone/XML/docs/Reference/eBay/GetNotificationsUsage.html
    FIX: timeout problem
    """

    method_name = "GetNotificationsUsage"

    def get_params(
        self,
        remote_id: str = None,
        start_time: str = None,
        end_time: str = None,
        hours_ago: int = None,
        **kwargs,
    ):
        if hours_ago:
            start_time = (datetime.now() - timedelta(hours=hours_ago)).isoformat()
            end_time = datetime.now().isoformat()
        elif not end_time:
            end_time = datetime.now().isoformat()

        return {
            "ItemID": remote_id,
            "StartTime": start_time,
            "EndTime": end_time,
        }


class SetNotificationSettings(EbayTradingAPI):
    """
    Docs:
    https://developer.ebay.com/Devzone/XML/docs/Reference/eBay/SetNotificationPreferences.html
    """

    method_name = "SetNotificationPreferences"

    def get_params(
        self,
        alert_enable: bool = None,
        app_enable: bool = None,
        alert_email: str = None,
        app_url: str = None,
        delivery_urls: dict = None,
        subscriptions: list = None,
        user_identifier: str = None,
        **kwargs,
    ):
        params = {
            "ApplicationDeliveryPreferences": {
                "AlertEmail": alert_email,
                "ApplicationURL": app_url,
                "DeviceType": "Platform",
            },
            "UserDeliveryPreferenceArray": subscriptions,
        }

        if app_enable is not None:
            params["ApplicationDeliveryPreferences"]["ApplicationEnable"] = "Enable" if app_enable else "Disable"

        if alert_enable is not None:
            params["ApplicationDeliveryPreferences"]["AlertEnable"] = "Enable" if alert_enable else "Disable"

        if user_identifier:
            params["UserData"] = {
                "ExternalUserData": user_identifier,
            }

        if delivery_urls:
            params["ApplicationDeliveryPreferences"].update(
                {
                    "DeliveryURLDetails": [
                        {
                            "DeliveryURL": url,
                            "DeliveryURLName": url,
                            "Status": "Enable" if enable else "Disable",
                        }
                        for url, enable in delivery_urls.items()
                    ]
                }
            )
            params["DeliveryURLName"] = ",".join(list(delivery_urls.keys()))

        return params


class ReviseNotifications(SetNotificationSettings):
    def get_params(self, notifications: list, enable: bool, **kwargs):
        for notification in notifications:
            assert (
                notification in PlatformNotificationEventTypeEnum
            ), f'Недопустимое значение "notification": {notification}'

        kwargs["subscriptions"] = [
            {
                "NotificationEnable": [
                    {
                        "EventType": notification,
                        "EventEnable": "Enable" if enable else "Disable",
                    }
                    for notification in notifications
                ]
            }
        ]
        return super().get_params(**kwargs)


class SubscribeNotification(ReviseNotifications):
    def get_params(self, **kwargs):
        kwargs["enable"] = True
        return super().get_params(**kwargs)


class UnSubscribeNotification(ReviseNotifications):
    def get_params(self, **kwargs):
        kwargs["enable"] = False
        return super().get_params(**kwargs)
