from authentication.views import (
    AuthLoginAPIView,
    AuthRefreshAPIView,
    AuthTokenBlacklistView,
)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django_ninja_sample.views import ninja_api
from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
    SpectacularYAMLAPIView,
)
from orders.views import OrderViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from stores.views import ContractViewSet, StoreViewSet
from users.views import UserViewSet

router = DefaultRouter()
# 해당 URL에 대한 요청을 적절한 ViewSet으로 매핑해주는 router
router.register(prefix=r"users", viewset=UserViewSet, basename="user")
# router.register(prefix="products", viewset=ProductViewSet, basename="product")
router.register(prefix="stores", viewset=StoreViewSet, basename="store")
router.register(prefix="orders", viewset=OrderViewSet, basename="order")
# prefix /user/로 매핑, viewset: views.py의 비즈니스 로직 처리, basename: url패턴 이름
""" 다음과 같은 URL 패턴을 만듬
GET /users/: 사용자 목록을 가져옵니다 (list).
POST /users/: 새로운 사용자를 만듭니다 (create).
GET /users/{pk}/: 특정 사용자의 세부 정보를 가져옵니다 (retrieve).
PUT /users/{pk}/: 특정 사용자를 업데이트합니다 (update).
PATCH /users/{pk}/: 특정 사용자를 부분 업데이트합니다 (partial_update).
DELETE /users/{pk}/: 특정 사용자를 삭제합니다 (destroy).
"""

store_nested_router = NestedDefaultRouter(router, "stores", lookup="store")
store_nested_router.register(prefix="contracts", viewset=ContractViewSet, basename="contract")

urlpatterns = [
                  # APP REST
                  path("api/", include(router.urls)),
                  path("api/", include(store_nested_router.urls)),
                  # authentication
                  path("api/token/", AuthLoginAPIView.as_view(), name="token_obtain_pair"),
                  path("api/token/refresh/", AuthRefreshAPIView.as_view(), name="token_refresh"),
                  path("api/token/blacklist/", AuthTokenBlacklistView.as_view(), name="token_blacklist"),
                  path("admin/", admin.site.urls),
                  # API Document
                  path("docs/json/", SpectacularJSONAPIView.as_view(), name="schema-json"),
                  path("docs/yaml/", SpectacularYAMLAPIView.as_view(), name="schema-yaml"),
                  # Open API Document with UI:
                  path("docs/", SpectacularSwaggerView.as_view(url_name="schema-json"), name="swagger-ui-default"),
                  path("docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema-json"), name="swagger-ui"),
                  path("docs/redoc/", SpectacularRedocView.as_view(url_name="schema-yaml"), name="redoc"),
                  # ninja sample
                  path("ninja-api/", ninja_api.urls)
              ] + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)  # type: ignore[arg-type]
