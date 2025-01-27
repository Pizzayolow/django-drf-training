from django.urls import path
from watchlist_app.api.views import (WatchListAV, WatchDetailAV, StreamPlatformAV, StreamPlatformDetailAV,
                                     ReviewList, ReviewDetail, ReviewCreate, Index)

urlpatterns = [
    
    path('', Index.as_view(), name="index"),
    
    # WATCHLIST
    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>', WatchDetailAV.as_view(), name='movie-details'),
    
    # STREAM PLATFORMS
    path('stream/', StreamPlatformAV.as_view(), name='stream'),
    path('stream/<int:pk>', StreamPlatformDetailAV.as_view(), name='streamplatform-detail'),
    
    # REVIEW
    # path('review/', ReviewList.as_view(), name='review-list'),
    # path('review/<int:pk>', ReviewDetail.as_view(), name='review-detail'),
    
    path('stream/<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('stream/<int:pk>/review/', ReviewList.as_view(), name='review-list'),
    path('stream/review/<int:pk>', ReviewDetail.as_view(), name='review-detail'),
]
