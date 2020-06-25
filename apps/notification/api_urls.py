from rest_framework_nested import routers

from . import viewsets

router = routers.DefaultRouter()

router.register('namespaces', viewsets.NamespaceViewSet)
router.register('subscribers', viewsets.SubscriberViewSet)

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

urlpatterns = router.urls
urlpatterns += namespace_router.urls
