from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from apps.audit.gdpr import anonymize_user, export_user_data

from .forms import CustomUserCreationForm


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_retention(years=2)
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect("/")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    return render(request, "accounts/profile.html")


@login_required
def export_data(request):
    """GDPR: export all personal data as JSON."""
    data = export_user_data(request.user)
    return JsonResponse(data, json_dumps_params={"indent": 2, "ensure_ascii": False})


@login_required
@require_POST
def delete_account(request):
    """GDPR: right to be forgotten — anonymize account."""
    anonymize_user(request.user)
    from django.contrib.auth import logout

    logout(request)
    return redirect("/")
