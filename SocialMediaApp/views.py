from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView, ListAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .mixins import CustomUserRateThrottle, ObjectPagination
from .models import FriendRequest, Useraccount
from .serializers import (
    AcceptRequestSerializer,
    ListFriendsSerializer,
    ListRequestsSerializer,
    LoginSerializer,
    SendRequestSerializer,
    UserSearchSerializer,
    UserSerializer,
)

# Create your views here.

"""  Handles the creation of User and associated Useraccount objects during the registration process.  """


class APIRegistrationView(GenericAPIView):
    allowed_methods = ["POST"]
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "Success": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""  Authenticates the user and manages the login process, including token creation and user validation. """


class APILoginView(GenericAPIView):
    allowed_methods = ["POST"]
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(
                email=serializer.validated_data.get("email")
            ).first()
            if user:
                username = str(user.username)
                password = serializer.validated_data.get("password")
                is_authenticated = authenticate(
                    username=username, password=password, request=request
                )
                if is_authenticated:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({"token": token.key}, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"error": "Incorrect Email or Password"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"error": "Incorrect Email or Password"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""  Handels the user search functionality. """


class SearchUsers(ListAPIView):
    allowed_methods = ["GET"]
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = ObjectPagination
    serializer_class = UserSearchSerializer

    def get_queryset(self):
        queryset = Useraccount.objects.exclude(user=self.request.user)

        search_param = self.request.GET.get("search_param", None)

        if search_param:
            if "@" in search_param:
                queryset = queryset.filter(user__email=search_param)
            else:
                queryset = queryset.filter(
                    Q(user__first_name__icontains=search_param)
                    | Q(user__last_name__icontains=search_param)
                    & ~Q(user=self.request.user)
                )

        return queryset


"""  The view is responsible for Handling the friend requests listing functionality. """


class ListRequests(ListAPIView):
    allowed_methods = ["GET"]
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = ObjectPagination
    serializer_class = ListRequestsSerializer

    def get_queryset(self):
        queryset = FriendRequest.objects.filter(
            to_usr__user=self.request.user, accept_status=False
        )
        return queryset


"""  The view is responsible for Handling the friends listing functionality. """


class ListFriends(ListAPIView):
    allowed_methods = ["GET"]
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = ObjectPagination
    serializer_class = ListFriendsSerializer

    def get_queryset(self):
        queryset = Useraccount.objects.prefetch_related("friends").get(
            user=self.request.user
        )
        return queryset.friends.all()


"""  The view is responsible for Handling the friends request accept and reject functionality. """


class AcceptRejectView(GenericAPIView):
    allowed_methods = ["POST", "DELETE"]
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = AcceptRequestSerializer

    """ Accept Request """

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"Success": "Successfully Accepted Friend Request"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """ Reject Request -- Note: This action will result in the permanent deletion of the request object, as soft deletion has not been implemented."""

    def delete(self, request, format=None):
        try:
            id = request.query_params.get("friend_request_id")
            request_obj = get_object_or_404(FriendRequest, pk=id, accept_status=False)
            request_obj.delete()
            return Response(
                {"Success": "Successfully Rejected Friend Request"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except FriendRequest.DoesNotExist:
            return Response({"error": "Oops....! Something Went Wrong"}, status=404)


"""  The view is responsible for Handling the friends request sending functionality. """


class SendRequestView(GenericAPIView):
    allowed_methods = ["GET", "POST", "DELETE"]
    throttle_classes = [CustomUserRateThrottle]
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = SendRequestSerializer

    """ Send Request """

    def post(self, request):
        serializer = self.get_serializer(data=request.data, request=request)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"Success": "Successfully Sended Friend Request"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
Handles the user logout process by deleting the user token.
"""


class APILogOutView(GenericAPIView):
    allowed_methods = ["POST"]
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            {"success": "Success fully logged out"}, status=status.HTTP_200_OK
        )
