from django.urls import path, include
from api.views import *

urlpatterns = [
    path('signup/', UserRegistrationView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('search/', SearchUserView.as_view(), name='search'),
    path('send-request/', SendFriendRequestView.as_view(), name='send-request'),
    path('respond-request/', RespondFriendRequestView.as_view(), name='respond-request'),
    path('friends/', ListFriendsView.as_view(), name='friends'),
    path('pending-requests/', ListPendingRequestsView.as_view(), name='pending-requests'),
]
