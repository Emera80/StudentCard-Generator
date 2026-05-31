from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('new/', views.etudiant_new, name="etudiant_new"),
    path("list/", views.etudiant_list, name="etudiant_list"),
    path("card/", views.carte_view, name="carte"),
    path("rechercher/", views.rechercher_etudiant, name="rechercher_etudiant"),
    path("verify/<str:qr_data>/", views.verify_qr_code, name="verify_qr"),
    path("edit/<path:matricule>/", views.etudiant_edit, name="etudiant_edit"),
    path("delete/<path:matricule>/", views.etudiant_delete, name="etudiant_delete"),
]
