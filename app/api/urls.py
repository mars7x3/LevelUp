from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views.director import ClientModelViewSet, StaffModelViewSet, OrderModelViewSet, OrderReadViewSet, \
    StatementListView, UpdateStatementView, OrderDetailView, PDFHSCodeView, PDFExtractView
from api.views.work import OTKWorkView, PackerWorkView, MarkerImagesView, MarkerWorkView, CreateStatementView
from api.views.receiver import OrderListView, ReceptionView

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

        path('receiver/order/list/', OrderListView.as_view()),
        path('receiver/reception/', ReceptionView.as_view()),

        path('otk/work/', OTKWorkView.as_view()),
        path('packer/work/', PackerWorkView.as_view()),
        path('marker/work/', MarkerWorkView.as_view()),
        path('marker/work/get/images/', MarkerImagesView.as_view()),
        path('marker/create/statement/', CreateStatementView.as_view()),

        path('director/statement/list/', StatementListView.as_view()),
        path('director/statement/update/', UpdateStatementView.as_view()),
        path('director/order/', OrderDetailView.as_view()),
        path('director/pdf/hs-code/', PDFHSCodeView.as_view()),
        path('director/pdf/wb-code/', PDFExtractView.as_view()),




        path('', include(router.urls)),
    ])),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)