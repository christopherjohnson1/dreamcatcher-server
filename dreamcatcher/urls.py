"""dreamcatcher URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from dreamcatcherapi.views.medication import Medications
from django.urls import path
from rest_framework import routers
from dreamcatcherapi.views import Comments, Dreams, DreamCatcherUsers, DreamMedications, DreamTypes, Exercises, Medications, MoonPhases, StressEvents
from django.conf.urls import include

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'comments', Comments, 'comment')
router.register(r'dreams', Dreams, 'dream')
router.register(r'dreamcatcherusers', DreamCatcherUsers, 'dreamcatcheruser')
router.register(r'dreammedications', DreamMedications, 'dreammedication')
router.register(r'dreamtypes', DreamTypes, 'dreamtype')
router.register(r'exercises', Exercises, 'exercise')
router.register(r'medications', Medications, 'medication')
router.register(r'moonphases', MoonPhases, 'moonphase')
router.register(r'stressevents', StressEvents, 'stressevent')

urlpatterns = [
    path('', include(router.urls)),
]
