from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from reports.views import ReviewListView, ReviewView

urlpatterns = [
    url(r'^reviews/$', login_required(ReviewListView.as_view()), name='reviews'),
    url(r'^review/(?P<pk>\d+)/$', login_required(ReviewView.as_view()), name='review'),
]
