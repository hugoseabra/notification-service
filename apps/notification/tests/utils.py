from model_mommy import mommy


def create_namespace(save=False, ignore_validation=False):
    """
    Creates a namespace instance.
    """
    instance = mommy.prepare('notification.Namespace')

    if save is True:
        if ignore_validation is False:
            instance.validate()

        instance.save(ignore_validation=ignore_validation)

    return instance


def create_group(save=False, ignore_validation=False):
    """
    Creates a group instance.
    """
    instance = mommy.prepare('notification.Group')

    namespace = create_namespace(save=True, ignore_validation=True)
    instance.namespace = namespace

    if save is True:
        if ignore_validation is False:
            instance.validate()

        instance.save(ignore_validation=ignore_validation)

    return instance


def create_subscriber(save=False, ignore_validation=False):
    """
    Creates a subscriber instance.
    """
    instance = mommy.prepare('notification.Subscriber')

    namespace = create_namespace(save=True, ignore_validation=True)
    instance.namespace = namespace

    if save is True:
        if ignore_validation is False:
            instance.validate()

        instance.save(ignore_validation=ignore_validation)

    return instance


def create_notification(save=False, ignore_validation=False):
    """
    Creates a notification instance.
    """
    instance = mommy.prepare('notification.Notification')

    subscriber = create_subscriber(save=True, ignore_validation=True)
    instance.subscriber = subscriber

    if save is True:
        if ignore_validation is False:
            instance.validate()

        instance.save(ignore_validation=ignore_validation)

    return instance


def create_device(save=False, ignore_validation=False):
    """
    Creates a notification instance.
    """
    instance = mommy.prepare('notification.Device')

    subscriber = create_subscriber(save=True, ignore_validation=True)
    instance.subscriber = subscriber

    if save is True:
        if ignore_validation is False:
            instance.validate()

        instance.save(ignore_validation=ignore_validation)

    return instance


def create_transmission(save=False, ignore_validation=False):
    """
    Creates a transmission instance.
    """
    instance = mommy.prepare('notification.Transmission')

    device = create_device(save=True, ignore_validation=True)
    instance.device = device

    notification = create_notification(save=False)
    notification.subscriber = device.subscriber
    notification.save(ignore_validation=True)

    instance.notification = notification

    if save is True:
        if ignore_validation is False:
            instance.validate()

        instance.save(ignore_validation=ignore_validation)

    return instance
