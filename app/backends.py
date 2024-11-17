# from django.contrib.auth.backends import ModelBackend

# from django.contrib.auth.models import User

# class EmailAuthentication(ModelBackend):
#     def authenticate (self,request,username=None, password=None, **kwargs):
#         if username is None:
#             username = kwargs.get('email')
#         try:
#             user = User.objects.get(username=username)

#             # if(User.objects.filter(username=email).exists()):
#             #     user= User.objects.get(username = email)
            
#             # else:
#             #     user= User.objects.get(email=username)

#             # if user.check_password(password):
#             #     user.backend = "%s.%s"%(self.__module__, self.__class__.__name__)
#             #     return user
            
#         except User.DoesNotExist:
#             try:
#                 user= User.objects.get(email = username)
#             except User.DoesNotExist:
#                 return None
        
#         if user.check_password(password) and self.user_can_authenticate(user):
#             return user
#         return None

# from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth.models import User

# class EmailOrUsernameBackend(ModelBackend):
#     """
#     Custom backend to authenticate with either username or email and password.
#     """
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             # Attempt to find the user by username or email
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             try:
#                 user = User.objects.get(email=username)
#             except User.DoesNotExist:
#                 return None

#         # Validate the password and check if the user is active
#         if user.check_password(password) and self.user_can_authenticate(user):
#             return user
#         return None


from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username = None, password = None, **kwargs):
        try:
            user= User.objects.get(email = username)

        except User.DoesNotExist:
            return None

        if user.check_password(password):
            print("user:{user.username} , Email: {user.email}")
            return user
        return None
        
        if user.check_password(passowrd):
            print(f"User:{user.username} , Email:{user.email}")
            return user

        return None    