from rest_framework_nested import routers

from . import viewsets

router = routers.DefaultRouter()

router.register('namespaces', viewsets.NamespaceViewSet)
router.register('subscribers', viewsets.SubscriberViewSet)
router.register('devices', viewsets.DeviceViewSet)
router.register('notifications', viewsets.NotificationViewSet)

# Namespace.
namespace_router = routers.NestedSimpleRouter(
    parent_router=router,
    parent_prefix='namespaces',
    lookup='namespace'
)
namespace_router.register(
    prefix='groups',
    viewset=viewsets.GroupViewSet,
    basename='namespace-groups'
)

# Subscriber.
subscriber_router = routers.NestedSimpleRouter(
    parent_router=router,
    parent_prefix='subscribers',
    lookup='subscriber'
)
subscriber_router.register(
    prefix='transmissions',
    viewset=viewsets.SubscriberTransmissionViewSet,
    basename='subscriber-transmissions'
)

# Device.
device_router = routers.NestedSimpleRouter(
    parent_router=router,
    parent_prefix='devices',
    lookup='device'
)
device_router.register(
    prefix='transmissions',
    viewset=viewsets.DeviceTransmissionViewSet,
    basename='device-transmissions'
)

# Notification.
notification_router = routers.NestedSimpleRouter(
    parent_router=router,
    parent_prefix='notifications',
    lookup='notification'
)
notification_router.register(
    prefix='transmissions',
    viewset=viewsets.NotificationTransmissionViewSet,
    basename='notification-transmissions'
)

urlpatterns = router.urls
urlpatterns += namespace_router.urls
urlpatterns += subscriber_router.urls
urlpatterns += device_router.urls
urlpatterns += notification_router.urls
