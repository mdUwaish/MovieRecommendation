from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.rest import Client

from .models import User
from .serializers import OTPSerializer, RegisterSerializer, UserSerializer
from .utils import get_tokens_for_user
from .helpers import send_forget_password_mail

import os
import random
import uuid

load_dotenv()

# Create your views here.
class Register(APIView):
    
    def post(self, request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class Login(APIView):

    def post(self, request):
        phone_number= request.data.get('phone_number')
        password=request.data.get('password')

        if not phone_number:
            return Response({'message':"Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not password:
            return Response({'message':"Password is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        
        user=authenticate(request, phone_number=phone_number, password=password)
        if user is None:
            return Response({'message':"Invalid Phone number or Password."}, status=status.HTTP_400_BAD_REQUEST)
        
        otp=random.randint(100000, 999999)

        try:
            client=Client(os.getenv("TWILIO_ACCOUNT_SID"),os.getenv("TWILIO_AUTH_TOKEN"))
            message=client.messages.create(
                body=f"Your verification code is {otp}",
                from_="+18635882598",
                to=phone_number
            )
            print(message)
            otp_timestamp = datetime.now().isoformat()
            request.session['otp'] = otp
            request.session['phone_number']= phone_number
            request.session['otp_timestamp'] = otp_timestamp

            return Response({'message':"OTP sent sucessfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':f"Failed to send OTP:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class verify_otp(APIView):

    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        otp = serializer.validated_data['otp']

        stored_otp = request.session.get('otp')
        stored_phone_number= request.session.get('phone_number')
        otp_timestamp_str = request.session.get('otp_timestamp')

        if not (stored_otp and stored_phone_number and otp_timestamp_str):
            # print("asdhjjfhgfsrtrdfdhgrdhgdfhhstdhhhfhgtsshg")
            return Response({"message": 'OTP has expired. Request a new one.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            otp_timestamp=datetime.fromisoformat(otp_timestamp_str)
        except ValueError:
            return Response({"message": 'Invalid OTP timestamp format.'}, status=status.HTTP_400_BAD_REQUEST)
        
        current_time = datetime.now()
        otp_expiration_time = otp_timestamp + timedelta(minutes=10)

        if current_time > otp_expiration_time:
            del request.session['otp']
            del request.session['phone_number']
            del request.session['otp_timestamp']
            return Response({"message": 'OTP has expired. Request a new one.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if otp == str(stored_otp):
            user = User.objects.get(phone_number = stored_phone_number)
            tokens = get_tokens_for_user(user)

            del request.session['otp']
            del request.session['phone_number']
            del request.session['otp_timestamp']
        
            return Response({'message': "Login successful.", 'tokens': tokens}, status=status.HTTP_200_OK)
        
        return Response({'message': "Invalid OTP or phone number."}, status=status.HTTP_400_BAD_REQUEST)
    

class Profile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    

class ProfileDetail(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ResetPassword(APIView):
    
    def post(self, request):
        phone_number=request.data.get('phone_number')

        user= User.objects.filter(phone_number=phone_number).first()

        if user is None:
            return Response({'message':"No user found."})
        
        token=str(uuid.uuid4())
        user.forget_password_token=token
        user.save()
        send_forget_password_mail(user.email, token)
        return Response({'message':"Email sent to the User."})
    

class UpdatePassword(APIView):

    def post(self, request, token):
        context= {}
        try:
            user= User.objects.filter(forget_password_token=token).first()
            context = {'user_id':user.user.id}
            new_password=request.data.get('new_password')
            confrim_password=request.data.get('confirm_password')
            phone_number=request.data.get('phone_number')

            if phone_number is None:
                return Response({'message':"No User found."})
            
            if new_password != confrim_password:
                return Response({'message':"Password not match."})
            
            user_obj= User.objects.filter(phone_number=phone_number)
            user_obj.set_password(new_password)
            user_obj.save()
        except Exception as e:
            return Response({'message':f"Error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)