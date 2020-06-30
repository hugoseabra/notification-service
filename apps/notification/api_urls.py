from rest_framework_nested import routers

from . import viewsets

router = routers.DefaultRouter()

router.register('namespaces', viewsets.NamespaceViewSet)
router.register('subscribers', viewsets.SubscriberViewSet)
router.register('devices', viewsets.DeviceViewSet)

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
    prefix='devices',
    viewset=viewsets.DeviceViewSet,
    basename='subscriber-devices'
)

subscriber_router.register(
    prefix='notifications',
    viewset=viewsets.NotificationViewSet,
    basename='subscriber-notifications'
)

subscriber_router.register(
    prefix='transmissions',
    viewset=viewsets.TransmissionViewSet,
    basename='subscriber-transmissions'
)

# Device.
device_router = routers.NestedSimpleRouter(
    parent_router=router,
    parent_prefix='devices',
    lookup='device'
)

device_router.register(
    prefix='subscribers',
    viewset=viewsets.SubscriberViewSet,
    basename='device-subscribers'
)

device_router.register(
    prefix='transmissions',
    viewset=viewsets.TransmissionViewSet,
    basename='device-transmissions'
)

urlpatterns = router.urls
urlpatterns += namespace_router.urls
urlpatterns += subscriber_router.urls
urlpatterns += device_router.urls