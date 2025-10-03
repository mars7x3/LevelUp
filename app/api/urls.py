from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views.director import ClientModelViewSet, StaffModelViewSet, OrderModelViewSet, OrderReadViewSet

router = DefaultRouter()
router.register('director/client/crud', ClientModelViewSet)
router.register('director/staff/crud', StaffModelViewSet)
router.register('director/order/crud', OrderModelViewSet)
router.register('director/order/read', OrderReadViewSet)




urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/', include([
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

        path('token/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),



        path('', include(router.urls)),
    ])),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)