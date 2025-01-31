from rest_framework import routers

from images import views
from images.apps import ImagesConfig

app_name = ImagesConfig.name

router = routers.DefaultRouter()
router.register("", views.ImagesViewSet, basename="images")

urlpatterns = router.urls
