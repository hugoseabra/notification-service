import onesignal as onesignal_sdk


class Client(onesignal_sdk.Client):
    def __init__(self, app_auth_key=None, app_id=None, **kwargs):
        super().__init__(app_auth_key=app_auth_key, app_id=app_id, **kwargs)

    @staticmethod
    def create_notification(data: dict):
        return onesignal_sdk.Notification(post_body=data)

    def create_and_send_notification(self, data: dict):
        notification = self.create_notification(data=data)
        return self.send_notification(notification=notification)
