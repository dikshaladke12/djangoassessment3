from django.urls import path
from app.views import Login,Home,Register,Logout,Forgotpassword,Resetpassword

urlpatterns = [
    path("", Login.as_view(), name= "Login"),
    path("Logout/",Logout.as_view(), name="Logout"),
    path('Home/',Home.as_view(),name="Home"),
    path("Register/",Register.as_view(), name= "Register"),
    path("Forgotpassword/",Forgotpassword.as_view(), name ="Forgotpassword"),
    path("reset/<uuid:uuid>",Resetpassword.as_view(), name ="Resetpassword"),

]