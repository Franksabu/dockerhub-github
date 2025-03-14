from django.db import models
from django.contrib.auth.models import User


class Budget(models.Model):
    designation = models.CharField(max_length=100)
    montant = models.BigIntegerField()
    description = models.TextField(max_length=100)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-id",)
        db_table = "budget_budget"

    def __str__(self):
        return f"{self.montant}"


class UniteMesure(models.Model):
    code = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=100)

    class Meta:
        ordering = ("-id",)
        db_table = "unite_depense"

    def __str__(self):
        return f"{self.code}"


class Depense(models.Model):
    name = models.CharField(max_length=30)
    montant = models.DecimalField(max_digits=10, decimal_places=2, default="0.00")
    numero_facture = models.CharField(max_length=50, null=True)
    file_facture = models.FileField(upload_to="media/facture", null=True, blank=True)
    description = models.TextField()
    date_depense = models.DateField()
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-id",)
        db_table = "operation_operation"

    def __str__(self):
        return f"{self.montant}"


class DetailDepense(models.Model):
    designation = models.CharField(max_length=100)
    quantite = models.DecimalField(max_digits=10, decimal_places=2, default="0")
    prix_unit = models.DecimalField(max_digits=10, decimal_places=2, default="0.00")
    prix_tot = models.DecimalField(max_digits=10, decimal_places=2, default="0.00")
    depense = models.ForeignKey(Depense, on_delete=models.CASCADE)
    unite_mesure = models.ForeignKey(UniteMesure, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return f"{self.designation}"


class Perte(models.Model):
    name = models.CharField(max_length=30)
    montant = models.BigIntegerField()
    description = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-id",)
        db_table = "perte_perte"

    def __str__(self):
        return f"{self.montant}"
