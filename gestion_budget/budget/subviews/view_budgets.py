from django.shortcuts import get_object_or_404, render, redirect
from budget.forms import *
from budget.models import Budget
from django.contrib.auth.models import User


def budget_create(request):
    if request.method == "POST":
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("budget_list")
    else:
        form = BudgetForm()
    return render(request, "budget/budget_create.html", {"form": form})


def budget_list(request):
    budgets = Budget.objects.all()
    return render(request, "budget/budget_list.html", {"budgets": budgets})


def budget_update(request, pk):
    budget = get_object_or_404(Budget, id=pk)

    if request.method == "POST":
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect("budget_list")
    else:
        form = BudgetForm(instance=budget)

    return render(
        request, "budget/budget_update.html", {"form": form, "budget": budget}
    )


def budget_delete(request, pk):
    budget = get_object_or_404(Budget, id=pk)
    budget.delete()
    return redirect("budget_list")


def user_list(request):
    # Récupérer tous les budgets
    budgets = Budget.objects.all()
    depenses = Depense.objects.all()
    pertes = Perte.objects.all()
    total_montant_budgets = sum(budget.montant for budget in budgets)
    total_montant_depenses = sum(depense.montant for depense in depenses)
    total_montant_pertes = sum(perte.montant for perte in pertes)
    #     total_montant_budgets = sum(budget.montant for budget in budgets)
    # Récupérer tous les utilisateurs
    users = User.objects.all()  # Récupère tous les objets du modèle User
    return render(
        request,
        "budget/user_list.html",
        {
            "users": users,
            "budgets": budgets,
            "depenses": depenses,
            "pertes": pertes,
            "total_montant_budgets": total_montant_budgets,
            "total_montant_depenses": total_montant_depenses,
            "total_montant_pertes": total_montant_pertes,
        },
    )
