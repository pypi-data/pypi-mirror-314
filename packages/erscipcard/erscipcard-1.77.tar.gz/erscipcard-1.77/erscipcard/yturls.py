from django.urls import path
from . import ytviews

urlpatterns = [
    path('', ytviews.helping ),
    path('download/<str:url>/<str:link>/', ytviews.viddown ),
    path('ytlink/', ytviews.vid ),
    path('shqr/', ytviews.shqr ),
    path('mp4/<str:link>/', ytviews.ytmp4 ),
    path('v/<str:url>/<str:link>/', ytviews.ytv ),
    path('p/<str:link>/', ytviews.ytp ),
    path('nginx/', ytviews.ngin ),
    path('<str:link>/', ytviews.ytdwn ),    
]
