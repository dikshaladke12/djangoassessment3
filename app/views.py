from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
import re
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.core.mail import send_mail
from django.utils.timezone import now
from django.conf import settings
import uuid
from datetime import timedelta
from .models import resetuuid
import datetime
from django.utils import timezone
import random


class Home(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, "Home.html")


class Login(View):
    def get(self, request):
        return render(request, "Login.html")

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            return render(request, "Login.html", {"error": "Email not matched"})

        user = authenticate(request, username=user.username, password=password)
        print(email, password)
        if user is not None:
            login(request, user)
            return redirect("Home/")
        else:
            print("invalid credentials")
            return render(request, "Login.html", {"errorLogin": "Invalid Credentials"})


class Register(View):
    def get(self, request):
        return render(request, "Register.html")

    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        print(username, password, confirm_password, email)

        if not username or not email or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return render(request, "register.html")

        if password != confirm_password:
            messages.error(request, "Password do not match")
            return render(request, "Register.html")

        if not self.validate_password(password):
            messages.error(
                request,
                "Password must be at least 8 character long and and include at least one uppercase letter, one lowercase letter, one number, and one special character.",
            )
            return render(request, "Register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return render(request, "Register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Email already registered")
            return render(request, "Register.html")

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Registration Successfull ! please login ")
        return redirect("/")

    def validate_password(self, password):
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"[0-9]", password):
            return False
        if not re.search(r"[@$!%*?&#]", password):
            return False
        return True


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("/")


class Forgotpassword(View):
    def get(self, request):
        return render(request, "Forgotpassword.html")

    def post(self, request):
        email = request.POST.get("email")

        if User.objects.filter(email=email).exists():

            user = User.objects.get(email=email)
            exp_date = timezone.now() + datetime.timedelta(hours=2)
            uuid_data = uuid.uuid1(random.randint(0, 281474976710655))

            forgot = resetuuid.objects.create(
                UUID=uuid_data, user=user, expiry=exp_date
            )

            url = f"{settings.SITE_URL}/resetpass/{forgot.UUID}"
            # print(url)
            if email:
                subject = "Password Reset Request"
                message = (
                    "To reset your password.Click the link below to get started:\n"
                    f"Rest your password\n\t{url}"
                )
                print(email)
                try:
                    print("jhhhhhhhhhhhhhhhhhhhhhhhh")
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
                    print("gjgfgfgfhgfhfcgf")
                    return redirect("/")
                except Exception as e:
                    return render(request, "Forgotpassword.html")

            else:
                return render(
                    request,
                    "Forgotpassword.html",
                    {"error": "failed to send the email"},
                )
        else:
            print(f"Invalid Email Address{email}")
            return render(request, "Forgotpassword.html")


class Resetpassword(View):
    def get(self, request, uuid):
        context = {"uuid": uuid}
        return render(request, "Resetpassword.html", context)

    def post(self, request, uuid):
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        current_date_time = datetime.datetime.now()

        obj = resetuuid.objects.get(UUID=uuid)
        user = obj.user
        # current_time = current_date_time.timezone('UTC')

        if password == confirm_password:
            user.set_password(password)
            user.save()
            return redirect("/")
        else:
            print("link expired")
            return redirect("/")
