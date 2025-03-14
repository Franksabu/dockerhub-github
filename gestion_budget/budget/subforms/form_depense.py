from django import forms
from budget.models import Depense, DetailDepense, UniteMesure


class DepenseForm(forms.ModelForm):
    class Meta:
        model = Depense
        fields = [
            "name",
            "montant",
            "numero_facture",
            "file_facture",
            "description",
            "date_depense",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "taper votre nom..."}
            ),
            "montant": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "montant depenser",
                    "min": "0",
                    "step": "0.01",
                }
            ),
            "numero_facture": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "numero de facture..."}
            ),
            "file_facture": forms.ClearableFileInput(
                attrs={"class": "form-control", "placeholder": "facture..."}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",  # Classe Bootstrap pour le style
                    "placeholder": "description depense...",
                    "rows": 3,  # Nombre de lignes
                    "cols": 20,  # Nombre de colonnes
                }
            ),
            "date_depense": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }

        labels = {
            "name": "Designation",
            "montant": "Montant",
            "numero_facture": "Numero de facture",
            "file_facture": "Fichier de facture",
            "description": "Description",
            "date_depense": "Date de depense",
        }


class DetailDepenseForm(forms.ModelForm):
    class Meta:
        model = DetailDepense
        fields = [
            "designation",
            "quantite",
            "prix_unit",
            "prix_tot",
            "depense",
            "unite_mesure",
            "description",
        ]
        widgets = {
            "designation": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "designation.."}
            ),
            "quantite": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "taper votre quantite...",
                }
            ),
            "depense": forms.HiddenInput(),
            "unite_mesure": forms.Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "Sélectionnez l'unite de mesure...",
                }
            ),
            "prix_unit": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "prix unitaire",
                    "min": "0",
                    "step": "0.01",
                }
            ),
            "prix_tot": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.01",
                    "readonly": "readonly",
                    "value": "0",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",  # Classe Bootstrap pour le style
                    "placeholder": "description detail depense...",
                    "rows": 3,  # Nombre de lignes
                    "cols": 20,  # Nombre de colonnes
                }
            ),
        }

        labels = {
            "designation": "Designation",
            "quantite": "Quantite",
            "prix_unit": "Prix unitaire",
            "prix_tot": "Prix total",
            "depense": "Depense",
            "unite_mesure": "Unite de mesure",
            "description": "Description",
        }

    def __init__(self, *args, **kwargs):
        self._depenceid = kwargs.pop("depenceid", None)
        super(DetailDepenseForm, self).__init__(*args, **kwargs)
        if self._depenceid is not None:
            self.fields["depense"].initial = self._depenceid


class UniteMesureForm(forms.ModelForm):
    class Meta:
        model = UniteMesure
        fields = [
            "nom",
            "code",
        ]

        widgets = {
            "nom": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "taper votre nom..."}
            ),
            "code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "taper le code de l'unite...",
                }
            ),
        }

        labels = {
            "nom": "Nom de l'unite",
            "code": "Code de l'unite",
        }
