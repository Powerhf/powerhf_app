from django.urls import path, include
from app.api.views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register('drf', EnergyFuelViewsets, basename='drf')
router.register('pre-monsoon', MonsoonChecklistViewset, basename='pmcl')

urlpatterns = [
    path('data-fuel/', include(router.urls)),
]