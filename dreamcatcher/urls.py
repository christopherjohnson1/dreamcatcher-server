"""dreamcatcher URL Configuration

"""
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from dreamcatcherapi.views import Comments, Dreams, DreamCatcherUsers, DreamMedications, DreamTypes
from dreamcatcherapi.views import Exercises, Medications, MoonPhases, StressEvents, Profiles
from dreamcatcherapi.views import login_user, register_user

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'comments', Comments, 'comment')
router.register(r'dreams', Dreams, 'dream')
router.register(r'dreamcatcherusers', DreamCatcherUsers, 'dreamcatcheruser')
router.register(r'dreammedications', DreamMedications, 'dreammedication')
router.register(r'dreamtypes', DreamTypes, 'dreamtype')
router.register(r'exercises', Exercises, 'exercise')
router.register(r'medications', Medications, 'medication')
router.register(r'moonphases', MoonPhases, 'moonphase')
router.register(r'profile', Profiles, 'profile')
router.register(r'stressevents', StressEvents, 'stressevent')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
