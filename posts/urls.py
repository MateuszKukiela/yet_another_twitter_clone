from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from posts import views

router = DefaultRouter()
router.register(r"posts", views.PostViewSet)
router.register(r"users", views.UserViewSet)

urlpatterns = [url(r"^", include(router.urls))]
