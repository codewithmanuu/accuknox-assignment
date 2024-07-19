from django.urls import path
from .views import APIRegistrationView, APILoginView, APILogOutView, SearchUsers, ListRequests, AcceptRejectView, SendRequestView, ListFriends

urlpatterns = [
    path('signup/',APIRegistrationView.as_view(),name='signup'),
    path('login/',APILoginView.as_view(),name='login'),
    path('logout/',APILogOutView.as_view(),name='logout'),
    path('search/',SearchUsers.as_view(),name='search'),
    path('friendrequests/',ListRequests.as_view(),name='friendrequests'),
    path('list-friends/', ListFriends.as_view(), name='list-friends'),
    path('accept-reject/',AcceptRejectView.as_view(),name='accept-reject'),
    path('send-request/',SendRequestView.as_view(),name='send-request'),
]