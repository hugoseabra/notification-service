from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from apps.notification import services
from apps.notification.models import Notification, Group


@receiver(post_save, sender=Notification)
def create_transmissions(instance, **_):
    services.create_transmissions(notification=instance)


@receiver(m2m_changed, sender=Notification.groups.through)
def prevent_group_from_different_namespace(action, instance, **kwargs):
    if action != 'pre_add':
        return

    pk_set = kwargs.pop('pk_set', list())
    model = kwargs.pop('model')

    if isinstance(instance, Notification) is True:
        # model variable is Group
        for group in model.objects.filter(pk__in=list(pk_set)):
            if str(group.namespace_id) != str(instance.namespace_id):
                raise Exception(
                    f'Group "{group}" and Notification "{instance}" are not'
                    f' from the same Namespace.'
                )

    elif isinstance(instance, Group) is True:
        # model variable is Subscriber
        for subscriber in model.objects.filter(pk__in=list(pk_set)):
            if str(subscriber.namespace_id) != str(instance.namespace_id):
                raise Exception(
                    f'Group "{instance}" and Notification "{subscriber}" are'
                    f' not from the same Namespace.'
                )
