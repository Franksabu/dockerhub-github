from datetime import datetime
from django.forms import ValidationError
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordChangeView,
    PasswordResetConfirmView,
)
from admin_coreui.forms import (
    RegistrationForm,
    LoginForm,
    UserPasswordResetForm,
    UserSetPasswordForm,
    UserPasswordChangeForm,
)
from django.views.generic import CreateView
from budget.models import Budget, Perte, Depense
from django.db.models import Sum, Count
from django.template.loader import get_template  # Importation correcte pour le modèle
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def get_context(request):
    # user_count = User.objects.all()
    active_users = User.objects.filter(is_active=True)
    somme_budgets = Budget.objects.aggregate(
        total_montant_budgets=Sum("montant"), total_budgets=Count("id")
    )
    somme_depenses = Depense.objects.aggregate(
        total_montant_depenses=Sum("montant"), total_depenses=Count("id")
    )
    somme_Pertes = Perte.objects.aggregate(
        total_montant_perte=Sum("montant"), total_pertes=Count("id")
    )

    # Récupérer les dates du formulaire, avec une valeur par défaut au format str
    # Autres traitements

    # Récupérer les dates du formulaire, avec une valeur par défaut
    date_debut = request.POST.get("dateDebut", timezone.now().date().isoformat()).strip()
    date_fin = request.POST.get("dateFin", timezone.now().date().isoformat()).strip()

    # date_encours = timezone.now().date()
    # budgets = Budget.objects.filter(date_create__date__range=[date_debut, date_fin])
    # depense = Depense.objects.filter(date_create__date__range=[date_debut, date_fin])
    # perte = Perte.objects.filter(date_create__date__range=[date_debut, date_fin])
    # total_montant_budgets_day = (budgets.aggregate(total_montant_budgets=Sum("montant")) or 0 )
    # total_montant_depenses_day = (depense.aggregate(total_montant_depenses=Sum("montant")) or 0)
    # total_montant_pertes_day = (perte.aggregate(total_montant_pertes=Sum("montant")) or 0)

    # user

    # total_users = user_count["total_users"] or 0  
    # active_users = active_users["User"]

    # bugdet, depnse et perte

    if date_debut and date_fin:
        budgets = Budget.objects.filter(date_create__date__range=[date_debut, date_fin])
        depenses = Depense.objects.filter(date_create__date__range=[date_debut, date_fin])
        pertes = Perte.objects.filter(date_create__date__range=[date_debut, date_fin])
        total_montant_budget = budgets.aggregate(total=Sum("montant"))["total"] or 0
        total_montant_depense = depenses.aggregate(total=Sum("montant"))["total"] or 0
        total_montant_perte = pertes.aggregate(total=Sum("montant"))["total"] or 0
    else:
        budgets = Budget.objects.all()
        depenses = Depense.objects.all()
        pertes = Perte.objects.all()
        total_montant_budget = somme_budgets["total_montant_budgets"] or 0
        total_montant_depense = somme_budgets["total_montant_depenses"] or 0
        total_montant_perte = somme_budgets["total_montant_pertes"] or 0

    total_budgets = somme_budgets["total_budgets"] or 0

    # budget
    total_montant_budgets = somme_budgets["total_montant_budgets"] or 0
    total_budgets = somme_budgets["total_budgets"] or 0
    # depense
    total_montant_depenses = somme_depenses["total_montant_depenses"] or 0
    total_depenses = somme_depenses["total_depenses"] or 0
    # perte
    total_montant_pertes = somme_Pertes["total_montant_perte"] or 0
    total_pertes = somme_Pertes["total_pertes"] or 0
    # reste
    reste = total_montant_budgets - (total_montant_depenses + total_montant_pertes)

    return {
        # "total_montant_budgets_day": total_montant_budgets_day,
        # "total_montant_depenses_day": total_montant_depenses_day,
        # "total_montant_pertes_day": total_montant_pertes_day,
        # "total_users": total_users,
        # "user_count": user_count,
        "active_users": active_users,
        "total_montant_budgets": total_montant_budgets,
        "total_montant_budget": total_montant_budget,
        "total_budgets": total_budgets,
        "total_montant_depenses": total_montant_depenses,
        "total_montant_depense": total_montant_depense,
        "total_depenses": total_depenses,
        "total_montant_pertes": total_montant_pertes,
        "total_montant_perte": total_montant_perte,
        "total_pertes": total_pertes,
        "budgets": budgets,
        "pertes": pertes,
        "depenses": depenses,
        "reste": reste,
    }


def get_data_to_print(request):
    data_get = get_context(request)
    budgets = data_get["budgets"]
    depenses = data_get["depenses"]
    pertes = data_get["pertes"]

    data = {
        "total_montant_budget": data_get["total_montant_budget"],
        "total_budgets": data_get["total_budgets"],
        "total_montant_depense": data_get["total_montant_depense"],
        "total_montant_perte": data_get["total_montant_perte"],
        "budgets": [
            {
                "designation": item.designation,
                "description": item.description,
                "montant": item.montant,
            }
            for item in budgets
        ],
        "pertes": [
            {
                "name": item.name,
                "description": item.description,
                "montant": item.montant,
            }
            for item in pertes
        ],
        "depenses": [
            {
                "name": item.name,
                "numero_facture": item.numero_facture,
                "montant": item.montant,
                "description": item.description,
            }
            for item in depenses
        ],
    }

    return JsonResponse(data)


def search_budgets(request):
    date_debut = request.GET.get("dateDebut")
    date_fin = request.GET.get("dateFin")
    
    if date_debut and date_fin:
        # Filtrer les budgets
        budgets = Budget.objects.filter(date_create__date__range=[date_debut, date_fin])
        budget_data = list(budgets.values())  # Convertir en liste de dictionnaires

        # Filtrer les dépenses
        depenses = Depense.objects.filter(date_create__date__range=[date_debut, date_fin])
        depense_data = list(depenses.values())  # Convertir en liste de dictionnaires

        # Filtrer les pertes
        pertes = Perte.objects.filter(date_create__date__range=[date_debut, date_fin])
        perte_data = list(pertes.values())  # Convertir en liste de dictionnaires

        # Retourner toutes les données sous forme de JSON
        return JsonResponse({
            'budgets': budget_data,
            'depenses': depense_data,
            'pertes': perte_data,
        }, safe=False)

    # Retourner une erreur si les dates sont invalides
    return JsonResponse({'error': 'Dates non valides'}, status=400)


@login_required(login_url="login")
def index(request):
    return render(request, "index.html", get_context(request))


@login_required(login_url="login")
def accordion(request):
    return render(request, "base/accordion.html")


@login_required(login_url="login")
def breadcrumb(request):
    return render(request, "base/breadcrumb.html")


@login_required(login_url="login")
def cards(request):
    return render(request, "base/cards.html")


@login_required(login_url="login")
def carousel(request):
    return render(request, "base/carousel.html")


@login_required(login_url="login")
def collapse(request):
    return render(request, "base/collapse.html")


@login_required(login_url="login")
def list_group(request):
    return render(request, "base/list-group.html")


@login_required(login_url="login")
def navs_tabs(request):
    return render(request, "base/navs-tabs.html")


@login_required(login_url="login")
def pagination(request):
    return render(request, "base/pagination.html")


@login_required(login_url="login")
def placeholders(request):
    return render(request, "base/placeholders.html")


@login_required(login_url="login")
def popovers(request):
    return render(request, "base/popovers.html")


@login_required(login_url="login")
def progress(request):
    return render(request, "base/progress.html")


@login_required(login_url="login")
def spinners(request):
    return render(request, "base/spinners.html")


@login_required(login_url="login")
def tables(request):
    return render(request, "base/tables.html")


@login_required(login_url="login")
def tooltips(request):
    return render(request, "base/tooltips.html")


@login_required(login_url="login")
def charts(request):
    return render(request, "charts.html")


@login_required(login_url="login")
def widgets(request):
    return render(request, "widgets.html")


@login_required(login_url="login")
def colors(request):
    return render(request, "colors.html")


@login_required(login_url="login")
def typography(request):
    return render(request, "typography.html")


@login_required(login_url="login")
def checks_radios(request):
    return render(request, "forms/checks-radios.html")


@login_required(login_url="login")
def floating_labels(request):
    return render(request, "forms/floating-labels.html")


@login_required(login_url="login")
def form_control(request):
    return render(request, "forms/form-control.html")


@login_required(login_url="login")
def input_group(request):

    return render(request, "forms/input-group.html")


@login_required(login_url="login")
def layout(request):
    return render(request, "forms/layout.html")


@login_required(login_url="login")
def range(request):
    return render(request, "forms/range.html")


@login_required(login_url="login")
def select(request):
    return render(request, "forms/select.html")


@login_required(login_url="login")
def validation(request):
    return render(request, "forms/validation.html")


@login_required(login_url="login")
def button_group(request):
    return render(request, "buttons/button-group.html")


@login_required(login_url="login")
def buttons(request):
    return render(request, "buttons/buttons.html")


@login_required(login_url="login")
def dropdowns(request):
    return render(request, "buttons/dropdowns.html")


@login_required(login_url="login")
def coreui_icons_brand(request):
    return render(request, "icons/coreui-icons-brand.html")


@login_required(login_url="login")
def coreui_icons_flag(request):
    return render(request, "icons/coreui-icons-flag.html")


@login_required(login_url="login")
def coreui_icons_free(request):
    return render(request, "icons/coreui-icons-free.html")


@login_required(login_url="login")
def alerts(request):
    return render(request, "notifications/alerts.html")


@login_required(login_url="login")
def badge(request):
    return render(request, "notifications/badge.html")


@login_required(login_url="login")
def modals(request):
    return render(request, "notifications/modals.html")


@login_required(login_url="login")
def toasts(request):
    return render(request, "notifications/toasts.html")


# auth
class UserRegistrationView(CreateView):
    template_name = "accounts/register.html"
    form_class = RegistrationForm
    success_url = "/accounts/login/"


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm


class UserPasswordResetView(PasswordResetView):
    template_name = "accounts/password-reset.html"
    form_class = UserPasswordResetForm


class UserPasswrodResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password-reset-confirm.html"
    form_class = UserSetPasswordForm


class UserPasswordChangeView(PasswordChangeView):
    template_name = "accounts/change-password.html"
    form_class = UserPasswordChangeForm


def logout_view(request):
    logout(request)
    return redirect("/accounts/login/")


def custom_404(request, exception):
    return render(request, "404.html", status=404)
