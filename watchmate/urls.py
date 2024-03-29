from django.contrib import admin
from django.urls import path, include
# from watchlist_app.views import ListIndex

import watchlist_app

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('index/', ListIndex.as_view(), name="list-index"),
    path('watch/', include('watchlist_app.api.urls')),
]
