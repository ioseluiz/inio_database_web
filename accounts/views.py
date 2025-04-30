from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import CustomUser

def SignUpView(request):
    pass

def SignInView(request):
    if request.method == "POST":
        # Get email and password from POST dictionary
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f"Bienvenido de nuevo, {user.username}!")
                    # Redirect to homepage
                    return redirect("home:home")
                else:
                    messages.warning(request, "El usuario no esta activo")
                    return redirect("accounts:sign-in")
            else:
                messages.warning(request, "El usuario no existe.")
                return("accounts:sign-in")
            
        except:
            messages.warning(request, "El usuario no existe.")

    return render(request, "accounts/sign-in.html")

def SignOutView(request):
    logout(request)
    messages.success(request, "Se ha salido la sesion.")
    return redirect("accounts:sign-in")
