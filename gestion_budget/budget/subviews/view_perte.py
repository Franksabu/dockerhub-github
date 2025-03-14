from django.shortcuts import get_object_or_404, render, redirect
from budget.forms import *
from budget.models import Perte


def create_perte(request):
    if request.method == "POST":
        form = PerteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("perte_list")
    else:
        form = PerteForm()
    return render(request, "perte/perte_create.html", {"form": form})


def perte_list(request):
    pertes = Perte.objects.all()
    return render(request, "perte/perte_list.html", {"pertes": pertes})


def perte_update(request, pk):
    perte = get_object_or_404(Perte, id=pk)

    if request.method == "POST":
        form = PerteForm(request.POST, instance=perte)
        if form.is_valid():
            form.save()
            return redirect("perte_list")
    else:
        form = PerteForm(instance=perte)

    return render(request, "perte/perte_update.html", {"form": form, "perte": perte})


def perte_delete(request, pk):
    perte = get_object_or_404(Perte, id=pk)
    perte.delete()
    return redirect("perte_list")
