from django.urls import path

from .views import OnlineUserListView


urlpatterns = [
    path("online-users/", OnlineUserListView.as_view(), name="online-users"),
]
