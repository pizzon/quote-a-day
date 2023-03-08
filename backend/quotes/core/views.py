from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login
from django.conf import settings
from django.contrib.auth.models import User
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken

from .models import Quotes, PhoneNumber, SecondaryEmail
from .serializers import QuoteSerializer, UserSerializer, RegisterSerializer

from rest_framework import viewsets
from .tasks import send_welcome_email_task
import requests
import os
import random


load_dotenv()
QUOTES_API_KEY = os.getenv("QUOTES_API_KEY")

QUOTES_API = "https://api.api-ninjas.com/v1/quotes?category="

QUOTES_CATEGORIES = ["happiness", "inspirational", "courage", "knowledge"]


class QuoteViewSet(viewsets.ModelViewSet):
    queryset = Quotes.objects.all()
    serializer_class = QuoteSerializer


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_welcome_email_task.delay(user.username, user.email)
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class UserAPI(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        user = self.request.user      
        return user
    
    def patch(self, request):
        user = self.request.user
        print(user, self.request.data)
        if 'phone_number' in self.request.data:
            PhoneNumber.objects.filter(user=user.id, phone_number=self.request.data['phone_number']).delete()
        if 'email' in self.request.data:
            SecondaryEmail.objects.filter(user=user.id, secondary_email=self.request.data['email']).delete()       
        return Response(UserSerializer(user).data)
    
    def put(self, request):
        user = self.request.user
        print(user, self.request.data)
        if 'phone_number' in self.request.data:
            num = PhoneNumber(phone_number=self.request.data['phone_number'], user=user)
            num.save()
        if 'email' in self.request.data:
            email = SecondaryEmail(secondary_email=self.request.data['email'], user=user)
            email.save()
        return Response(UserSerializer(user).data)
    

def add_quote_to_db(quote_data):
    quote_entry = Quotes(quote=quote_data["quote"], author=quote_data["author"])
    quote_entry.save()


def get_quote(request):
    response = requests.get(
        f"{QUOTES_API}{random.choice(QUOTES_CATEGORIES)}",
        headers={"X-Api-Key": QUOTES_API_KEY},
    )
    print(response.json())
    add_quote_to_db(response.json()[0])
    return JsonResponse(response.json()[0])
