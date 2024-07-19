from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from .mixins import create_user_name, has_digit
from .models import FriendRequest, Useraccount


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]
        username = create_user_name()

        if password != password2:
            raise serializers.ValidationError({"error": "password does't match"})
        if User.objects.filter(email=self.validated_data["email"]).exists():
            raise serializers.ValidationError({"error": "Email already exists"})

        if has_digit(str(self.validated_data["first_name"])):
            raise serializers.ValidationError(
                {"error": "Firstname Should only contain characters"}
            )
        elif has_digit(str(self.validated_data["last_name"])):
            raise serializers.ValidationError(
                {"error": "Lastname Should only contain characters"}
            )

        user = User(
            username=username,
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            email=self.validated_data["email"],
        )
        user.set_password(password)
        user.save()
        Useraccount.objects.create(user=user)

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)


class UserSearchSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="id")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = Useraccount
        fields = ["user_id", "first_name", "last_name", "email"]


class AcceptRequestSerializer(serializers.Serializer):
    friend_request_id = serializers.IntegerField()

    def save(self):
        try:

            id = self.validated_data["friend_request_id"]
            request__obj = FriendRequest.objects.get(id=id, accept_status=False)
            request__obj.accept_status = True
            frm_user = request__obj.frm_usr
            to_user = request__obj.to_usr
            frm_user.friends.add(to_user)
            to_user.friends.add(frm_user)
            request__obj.save()

        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                {"error": "Oops...! Something Went Wrong"}
            )


class SendRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(SendRequestSerializer, self).__init__(*args, **kwargs)

    def save(self):
        try:

            sender = self.request.user
            reciever_id = self.validated_data["user_id"]
            frm_usr = Useraccount.objects.get(user=sender)
            to_usr = Useraccount.objects.get(id=reciever_id)
            friends = frm_usr.friends.all().values_list("id", flat=True)
            if to_usr.id in friends:
                raise serializers.ValidationError(
                    {
                        "error": f"{to_usr.user.first_name} {to_usr.user.last_name}  is already in your friends list."
                    }
                )
            if frm_usr == to_usr:
                raise serializers.ValidationError(
                    {"error": f"You can't send friend reequest to your self."}
                )
            else:
                pending_frm_request = FriendRequest.objects.filter(
                    frm_usr=to_usr, to_usr=frm_usr
                ).first()
                pending_to_request = FriendRequest.objects.filter(
                    frm_usr=frm_usr, to_usr=to_usr
                ).first()
                if pending_frm_request:
                    raise serializers.ValidationError(
                        {
                            "error": f"{to_usr.user.first_name} {to_usr.user.last_name}  is awaiting your acceptance of his friend request."
                        }
                    )
                elif pending_to_request:
                    raise serializers.ValidationError(
                        {"error": f"Request already sended."}
                    )
                FriendRequest.objects.get_or_create(frm_usr=frm_usr, to_usr=to_usr)

        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                {"error": "Oops...! Something Went Wrong"}
            )


class ListRequestsSerializer(serializers.ModelSerializer):
    friend_request_id = serializers.IntegerField(source="id")
    first_name = serializers.CharField(source="frm_usr.user.first_name")
    last_name = serializers.CharField(source="frm_usr.user.last_name")
    email = serializers.EmailField(source="frm_usr.user.email")

    class Meta:
        model = FriendRequest
        fields = ["friend_request_id", "first_name", "last_name", "email"]


class ListFriendsSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="id")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = Useraccount
        fields = ["user_id", "first_name", "last_name", "email"]
