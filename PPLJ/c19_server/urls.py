from django.urls import path, include
from rest_framework.routers import DefaultRouter
from c19_server.views import FormViewSet, UserIDViewSet, UserViewSet, UserPhoneViewSet
from rest_framework_extensions.routers import NestedRouterMixin


class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass


router = NestedDefaultRouter()
user_router = router.register('users', UserPhoneViewSet, basename='userphone')
userid_router = user_router.register('userids', UserIDViewSet, basename='userphone-userid',
                                     parents_query_lookups=['userphone'])
userid_router.register('forms', FormViewSet, basename='userphone-userid-form',
                       parents_query_lookups=['userid__userphone', 'userid'])
router.register('owner', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
