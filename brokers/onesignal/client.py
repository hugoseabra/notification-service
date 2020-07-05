import onesignal as onesignal_sdk

from ..broker import Broker


class Client(Broker, onesignal_sdk.Client):
    def __init__(self, api_key=None, app_id=None, **kwargs):
        super().__init__(app_auth_key=api_key, app_id=app_id, **kwargs)

    @staticmethod
    def create_notification(data: dict):
        return onesignal_sdk.Notification(post_body=data)

    def create_and_send_notification(self, data: dict):
        notification = self.create_notification(data=data)
        return self.send_notification(notification=notification)
