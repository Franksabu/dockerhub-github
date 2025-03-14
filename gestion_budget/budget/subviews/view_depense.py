from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from budget.forms import *
from budget.models import Depense, DetailDepense
from django.db import transaction

# from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def create_depense(request):
    if request.method == "POST":
        form = DepenseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("depense_list")
    else:
        form = DepenseForm()
        return render(request, "depense/depense_create.html", {"form": form})


def depense_list(request):
    depenses = Depense.objects.all()
    return render(request, "depense/depense_list.html", {"depenses": depenses})


def depense_update(request, pk):
    depense = get_object_or_404(Depense, id=pk)

    if request.method == "POST":
        form = DepenseForm(request.POST, request.FILES, instance=depense)
        if form.is_valid():
            form.save()
            return redirect("depense_list")
    else:
        form = DepenseForm(instance=depense)

    return render(
        request, "depense/depense_update.html", {"form": form, "depense": depense}
    )


def depense_delete(request, pk):
    depense = get_object_or_404(Depense, id=pk)
    depense.delete()
    return redirect("depense_list")


# -------------------views pour detail depense-------------------------


def detail_depense_view(request, id):
    # Récupérer la dépense par son ID
    depense = get_object_or_404(Depense, id=id)
    # Récupérer tous les détails de cette dépense
    details_depense = DetailDepense.objects.filter(depense=depense)
    form = DetailDepenseForm(depenceid=id)

    if request.method == "POST":
        form = DetailDepenseForm(request.POST, depenceid=id)
        if form.is_valid():  # Vérifiez si le formulaire est valide
            with transaction.atomic():  # Commence une transaction atomique
                montant = form.cleaned_data.get("prix_tot")

                # Mettre à jour le montant de la dépense
                depense.montant += montant
                depense.save()

                # Sauvegarde du formulaire
                detail_depense_instance = form.save(commit=False)
                detail_depense_instance.depense = depense
                detail_depense_instance.save()
            success_url = f"/detail_depense/list/{id}/"
            return redirect(success_url)

    context = {
        "form": form,
        "depense": depense,
        "details_depense": details_depense,
    }
    return render(request, "depense/detail_depense_create.html", context)


def detail_depense_update(request, depense_id, detail_id):
    # Récupérer la dépense par son ID
    depense = get_object_or_404(Depense, id=depense_id)
    # Récupérer le détail de dépense à mettre à jour
    detail_depense_instance = get_object_or_404(
        DetailDepense, id=detail_id, depense=depense
    )

    # Initialiser le formulaire avec l'instance existante
    form = DetailDepenseForm(instance=detail_depense_instance)

    if request.method == "POST":
        form = DetailDepenseForm(request.POST, instance=detail_depense_instance)
        if form.is_valid():
            with transaction.atomic():
                montant = form.cleaned_data.get("prix_tot")
                # Ajuster le montant total de la dépense
                depense.montant += montant  # Ajouter le nouveau montant
                depense.save()

                # Sauvegarde du formulaire
                detail_depense_instance = form.save(commit=False)
                detail_depense_instance.depense = depense
                detail_depense_instance.save()
            return redirect(reverse("detail_depense_list", args=[depense_id]))

    context = {
        "form": form,
        "depense": depense,
        "detail_depense_instance": detail_depense_instance,
    }
    return render(request, "depense/detail_depense_update.html", context)


def detail_depense_delete(request, id, detail_id):
    # Récupérer la dépense associée
    depense = get_object_or_404(Depense, id=id)

    # Récupérer l'instance de DetailDepense à supprimer
    detail_depense_instance = get_object_or_404(
        DetailDepense, id=detail_id, depense=depense
    )
    # Supprimer l'instance de DetailDepense
    detail_depense_instance.delete()

    # Rediriger vers la liste des détails
    return redirect(f"/detail_depense/list/{id}/")


def detail_depense_list(request, id):
    depense = get_object_or_404(Depense, id=id)
    detail_depense = DetailDepense.objects.filter(depense_id=depense.id)
    for detail in detail_depense:
        detail.prix_tot = detail.prix_unit * detail.quantite  # Calculer le prix total
    context = {
        "depense": depense,
        "detail_depense": detail_depense,
    }
    return render(
        request,
        "depense/detail_depense_list.html",
        context,
    )


# ####################### vue pour unite de mesure ###################### #


def unite_mesure_create(request):
    if request.method == "POST":
        form = UniteMesureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("unite_mesure_list")
    else:
        form = UniteMesureForm()
        return render(request, "depense/unite_mesure_create.html", {"form": form})


def unite_mesure_list(request):
    unites = UniteMesure.objects.all()
    return render(request, "depense/unite_mesure_list.html", {"unites": unites})


def unite_mesure_update(request, pk):
    unite = get_object_or_404(UniteMesure, id=pk)

    if request.method == "POST":
        form = UniteMesureForm(request.POST, instance=unite)
        if form.is_valid():
            form.save()
            return redirect("unite_mesure_list")
    else:
        form = UniteMesureForm(instance=unite)

    return render(
        request, "depense/unite_mesure_update.html", {"form": form, "unite": unite}
    )


def unite_mesure_delete(request, pk):
    unite = get_object_or_404(UniteMesure, id=pk)
    unite.delete()
    return redirect("unite_mesure_list")
