from django import forms
from budget.models import Budget


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ["designation", "montant", "description"]

        widgets = {
            "designation": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "designation..."}
            ),
            "montant": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Entrez le montant",
                    "min": "0",  # Valeur minimale
                    "step": "0.01",  # Valeur d'incrément
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",  # Classe Bootstrap pour le style
                    "placeholder": "description budgetaire...",
                    "rows": 3,  # Nombre de lignes
                    "cols": 20,  # Nombre de colonnes
                }
            ),
        }

        labels = {
            "designation": "Designation",
            "montant": "Montant",
            "description": "Description",
        }
