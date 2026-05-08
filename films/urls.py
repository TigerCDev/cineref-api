from rest_framework.routers import DefaultRouter
from .views import CinematographerViewSet, FilmViewSet

router = DefaultRouter()
router.register(r'cinematographers', CinematographerViewSet)
router.register(r'films', FilmViewSet)

urlpatterns = router.urls