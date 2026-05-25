from rest_framework.routers import DefaultRouter
from .views import (
    CinematographerViewSet,
    FilmViewSet,
    LensViewSet,
    ShotViewSet,
    LightingSetupViewSet,
)

router = DefaultRouter()
router.register(r'cinematographers', CinematographerViewSet)
router.register(r'films', FilmViewSet)
router.register(r'lenses', LensViewSet)
router.register(r'shots', ShotViewSet)
router.register(r'lightingsetups', LightingSetupViewSet)

urlpatterns = router.urls