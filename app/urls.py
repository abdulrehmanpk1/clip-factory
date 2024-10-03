from django.urls import path

from . import views


urlpatterns = [
    path('video/process/', views.VideoProcessingView.as_view(),),
]
