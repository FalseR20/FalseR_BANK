from django.shortcuts import redirect, render


def index(request):
    if not request.user.is_authenticated:
        return render(request, "guest.html")

    if request.user.is_staff:
        return redirect("/admin")

    return render(request, 'frontend/home.html')
