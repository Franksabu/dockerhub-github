from django.contrib import admin
from .models import Budget, Depense, Perte, UniteMesure  # Import the models explicitly

# Register your models here.
admin.site.register(Budget)
admin.site.register(Depense)
admin.site.register(Perte)
admin.site.register(UniteMesure)
