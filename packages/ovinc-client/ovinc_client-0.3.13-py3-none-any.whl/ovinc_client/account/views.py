from channels.db import database_sync_to_async
from django.contrib import auth
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response

from ovinc_client.account.exceptions import VerifyFailed
from ovinc_client.account.models import User
from ovinc_client.account.serializers import UserInfoSerializer, UserSignInSerializer
from ovinc_client.core.auth import OAuthBackend, SessionAuthenticate
from ovinc_client.core.viewsets import ListMixin, MainViewSet

USER_MODEL: User = get_user_model()


class UserInfoViewSet(ListMixin, MainViewSet):
    """
    User Info
    """

    queryset = USER_MODEL.objects.all()

    async def list(self, request, *args, **kwargs):
        """
        User Info
        """

        return Response(await UserInfoSerializer(request.user).adata)


class UserSignViewSet(MainViewSet):
    """
    User Sign
    """

    queryset = USER_MODEL.objects.all()
    authentication_classes = [SessionAuthenticate]

    @action(methods=["POST"], detail=False)
    async def sign_in(self, request, *args, **kwargs):
        """
        Sign In
        """

        # verify
        request_serializer = UserSignInSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        request_data = request_serializer.validated_data

        # auth
        user = await OAuthBackend().authenticate(request, code=request_data["code"])
        if user:
            await database_sync_to_async(auth.login)(request, user)
            return Response()

        raise VerifyFailed()

    @action(methods=["GET"], detail=False)
    async def sign_out(self, request, *args, **kwargs):
        """
        Sign Out
        """

        await database_sync_to_async(auth.logout)(request)
        return Response()
