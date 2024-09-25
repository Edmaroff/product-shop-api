from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.serializers import RegisterUserSerializer


@extend_schema(
    tags=["Users"],
    summary="Регистрация нового пользователя",
    responses={201: "Пользователь успешно зарегистрирован"},
)
class RegistrationAPIView(APIView):

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            refresh.payload.update(
                {
                    "user_id": user.id,
                    "username": user.username,
                }
            )

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"Status": False, "Errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
