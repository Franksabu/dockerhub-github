from django import forms
from budget.models import Perte


class PerteForm(forms.ModelForm):
    class Meta:
        model = Perte
        fields = ['name', 'montant', 'description']

        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control", "placeholder": "tapez votre nom ici..."}),
            'montant': forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "tapez le montant de perte..",
                    "min": "0",
                    "step": "0.01"
                }),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "description depense...",
                    "rows": 3,
                    "cols": 20,
                }
            ),
        }
