
class Broker:
    """ Defines broker operations as a MUST to be implmented. """
    @staticmethod
    def create_notification(data: dict):
        raise NotImplementedError()

    def create_and_send_notification(self, data: dict):
        raise NotImplementedError()
