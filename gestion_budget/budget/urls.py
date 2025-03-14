from django.urls import path

from .views import *

urlpatterns = [
    # budget url
    path("budget/create/", budget_create, name="budget_create"),
    path("budget/", budget_list, name="budget_list"),
    path("budget/update/<int:pk>/", budget_update, name="budget_update"),
    path("budget/<int:pk>/delete/", budget_delete, name="budget_delete"),
    # depense urls
    path("depense/create/", create_depense, name="create_depense"),
    path("depense/", depense_list, name="depense_list"),
    path("depense/update/<int:pk>/", depense_update, name="depense_update"),
    path("depense/<int:pk>/delete/", depense_delete, name="depense_delete"),
    # perte urls
    path("perte/create/", create_perte, name="create_perte"),
    path("perte/", perte_list, name="perte_list"),
    path("perte/update/<int:pk>/", perte_update, name="perte_update"),
    path("perte/<int:pk>/delete/", perte_delete, name="perte_delete"),
    # path('budget_report/', budget_report, name='budget_report'),
    path("user_list/", user_list, name="user_list"),
    path("detail_depense/<int:id>/", detail_depense_view, name="detail_depense_view"),
    path('detail_depense/update/<int:depense_id>/<int:detail_id>/', detail_depense_update, name='detail_depense_update'),
    path('detail_depense/delete/<int:id>/<int:detail_id>/', detail_depense_delete, name='detail_depense_delete'),  # Ajoutez cette ligne
    path("detail_depense/list/<int:id>/", detail_depense_list, name="detail_depense_list"),
    path("unite_mesure/create/", unite_mesure_create, name="unite_mesure_create"),
    path("unite_mesure/list/", unite_mesure_list, name="unite_mesure_list"),
    path("unite_mesure/update/<int:pk>/", unite_mesure_update, name="unite_mesure_update"),
    path("unite_mesure/delete/<int:pk>/", unite_mesure_delete, name="unite_mesure_delete"),
]
