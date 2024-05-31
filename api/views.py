from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from api.serializers import (UserRegistrationSerializer, UserLoginSerializer,
                             UserProfileSerializer, UserSerializer, FriendRequestSerializer)
from api.renderers import UserRenderer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from api.models import User, FriendRequest
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class SearchUserPagination(PageNumberPagination):
    page_size = 10  # Page size
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token': token, 'msg': 'Registration Success'}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        print(request.user, "--------------")
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchUserView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    pagination_class = SearchUserPagination

    def get_queryset(self):
        keyword = self.request.query_params.get('q', '')
        return User.objects.filter(Q(email__icontains=keyword) | Q(name__iexact=keyword))


class SendFriendRequestView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        to_user_id = request.data.get('to_user_id')
        to_user = User.objects.get(id=to_user_id)
        from_user = request.user

        # Check if from_user is the same as to_user
        if from_user == to_user:
            return Response({"error": "You cannot send a friend request to yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Check rate limiting
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        if FriendRequest.objects.filter(from_user=from_user, timestamp__gte=one_minute_ago).count() >= 3:
            return Response({"error": "You cannot send more than 3 friend requests within a minute."},
                            status=status.HTTP_429_TOO_MANY_REQUESTS)

        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response({"error": "Friend request already sent."}, status=status.HTTP_400_BAD_REQUEST)

        friend_request = FriendRequest.objects.create(
            from_user=from_user, to_user=to_user)
        return Response({"message": "Friend request sent."}, status=status.HTTP_201_CREATED)


class RespondFriendRequestView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        friend_request_id = request.data.get('friend_request_id')
        action = request.data.get('action')
        friend_request = FriendRequest.objects.get(id=friend_request_id)

        # Check if the requesting user is the to_user of the friend request
        if request.user != friend_request.to_user:
            return Response({'error': 'You are not authorized to perform this action'}, status=status.HTTP_403_FORBIDDEN)

        if action not in ['accept', 'reject']:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

        if action == 'accept':
            friend_request.status = 'accepted'
        elif action == 'reject':
            friend_request.status = 'rejected'

        friend_request.save()
        return Response(FriendRequestSerializer(friend_request).data)


class ListFriendsView(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        print(user, "$$$$$$$$$$$$$$$")
        friends = FriendRequest.objects.filter(
            Q(from_user=user, status='accepted') |
            Q(to_user=user, status='accepted')
        )
        friend_ids = [f.to_user.id if f.from_user ==
                      user else f.from_user.id for f in friends]
        return User.objects.filter(id__in=friend_ids)


class ListPendingRequestsView(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        print(user, "&&&&&&&&&&&")
        return FriendRequest.objects.filter(to_user=user, status='pending')
