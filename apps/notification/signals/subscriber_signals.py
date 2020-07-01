from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from apps.notification.models import Subscriber, Group


@receiver(m2m_changed, sender=Subscriber.groups.through)
def prevent_group_from_different_namespace(action, instance, **kwargs):
    if action != 'pre_add':
        return

    pk_set = kwargs.pop('pk_set', list())
    model = kwargs.pop('model')

    if isinstance(instance, Subscriber) is True:
        # model variable is Group
        for group in model.objects.filter(pk__in=list(pk_set)):
            if str(group.namespace_id) != str(instance.namespace_id):
                raise Exception(
                    f'Group "{group}" and Subscriber "{instance}" are not'
                    f' from the same Namespace.'
                )

    elif isinstance(instance, Group) is True:
        # model variable is Subscriber
        for subscriber in model.objects.filter(pk__in=list(pk_set)):
            if str(subscriber.namespace_id) != str(instance.namespace_id):
                raise Exception(
                    f'Group "{instance}" and Subscriber "{subscriber}" are not'
                    f' from the same Namespace.'
                )
