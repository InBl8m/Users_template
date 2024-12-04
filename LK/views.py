from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ExampleView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve a list of items",
        responses={200: openapi.Response('A list of items', openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING)))}
    )
    def get(self, request):
        return Response(["item1", "item2", "item3"])


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user = authenticate(request, username=user.username, password=request.data['password'])
            if user is not None:
                login(request, user)
                return Response({"message": "User registered and logged in successfully."},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Authentication failed"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({"message": "User logged in successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})


def logout_view(request):
    logout(request)
    return redirect('login')
