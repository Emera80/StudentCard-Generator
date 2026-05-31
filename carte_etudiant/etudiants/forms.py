from django import forms
from .models import Etudiant

class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = [
            "matricule",
            "nom_etudiant",
            "prenom_etudiant",
            "postnom_etudiant",
            "sexe",
            "date_naissance",
            "lieu_naissance",
            "faculte",
            "promotion",
        ]
        widgets = {
            "matricule": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex: 24ABC1234",
                "id": "matriculeInput",
            }),
            "nom_etudiant": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nom",
            }),
            "prenom_etudiant": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Prénom",
            }),
            "postnom_etudiant": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Postnom",
            }),
            "sexe": forms.Select(attrs={
                "class": "form-select",
            }),
            "date_naissance": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),
            "lieu_naissance": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Lieu de naissance",
            }),
            "faculte": forms.Select(attrs={
                "class": "form-select",
            }),
            "promotion": forms.Select(attrs={
                "class": "form-select",
            }),
        }
