import qrcode
from io import BytesIO
from django.shortcuts import render , redirect, get_object_or_404
import urllib.parse
from django.http import JsonResponse
from django.http import HttpResponse
from .forms import EtudiantForm
from .models import Etudiant
import base64
# Create your views here.
# def home(request):
#     return render(request, 'etudiants/home.html')  # Chemin corrigé

def home(request):
    return render(request, 'home.html')  # Enlever 'etudiants/'

from django.shortcuts import render, redirect
from .forms import EtudiantForm
from .models import Etudiant

# def etudiant_list(request):
#     etudiants = Etudiant.objects.select_related("promotion__section__faculte").order_by("promotion__nom", "nom")
#     return render(request, "etudiants/list.html", {"etudiants": etudiants})

def etudiant_list(request):
    etudiants = Etudiant.objects.all().order_by("nom_etudiant")
    return render(request, "list.html", {"etudiants": etudiants})


def etudiant_new(request):
    if request.method == "POST":
        form = EtudiantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = EtudiantForm()
    return render(request, "form.html", {"form": form})


def carte_view(request):
    return render(request, "card.html")


def etudiant_edit(request, matricule):
    etudiant = get_object_or_404(Etudiant, pk=matricule)
    if request.method == "POST":
        form = EtudiantForm(request.POST, instance=etudiant)
        if form.is_valid():
            form.save()
            return redirect("etudiant_list")
    else:
        form = EtudiantForm(instance=etudiant)
    return render(request, "form.html", {"form": form, "etudiant": etudiant})


def etudiant_delete(request, matricule):
    etudiant = get_object_or_404(Etudiant, pk=matricule)
    if request.method == "POST":
        etudiant.delete()
        return redirect("etudiant_list")
    # For security, avoid deleting via GET; redirect back
    return redirect("etudiant_list")

# def rechercher_etudiant(request):
#     matricule = request.GET.get("matricule")
#     try:
#         etudiant = Etudiant.objects.get(matricule=matricule)
#         data = {
#             "matricule": etudiant.matricule,
#             "nom": etudiant.nom_etudiant,
#             "postnom": etudiant.postnom_etudiant,
#             "prenom": etudiant.prenom_etudiant,
#             "sexe": etudiant.sexe,
#             "date_naissance": str(etudiant.date_naissance),
#             "lieu_naissance": etudiant.lieu_naissance,
#             "promotion": etudiant.promotion.description_promotion,
#             "faculte": etudiant.faculte.description_faculte,
#             "section": etudiant.faculte.section.description_section,	
#         }
#         return JsonResponse({"success": True, "etudiant": data})
#     except Etudiant.DoesNotExist:
#         return JsonResponse({"success": False, "message": "Aucun étudiant trouvé"})

def rechercher_etudiant(request):
    matricule = request.GET.get("matricule")
    
    if not matricule:
        return JsonResponse({"success": False, "message": "Veuillez entrer un matricule"})
    
    try:
        etudiant = Etudiant.objects.get(matricule=matricule)
        data = {
            "matricule": etudiant.matricule,
            "nom": etudiant.nom_etudiant,
            "postnom": etudiant.postnom_etudiant,
            "prenom": etudiant.prenom_etudiant,
            "sexe": etudiant.sexe,
            "date_naissance": str(etudiant.date_naissance),
            "lieu_naissance": etudiant.lieu_naissance,
            "promotion": etudiant.promotion.description_promotion,
            "faculte": etudiant.faculte.description_faculte,
            "section": etudiant.faculte.section.description_section, 
            "qr_code_url": etudiant.qr_code.url if etudiant.qr_code else None,   
        }
        return JsonResponse({"success": True, "etudiant": data})
    except Etudiant.DoesNotExist:
        return JsonResponse({"success": False, "message": "Aucun étudiant trouvé avec ce matricule"})
    
def verify_qr_code(request, qr_data):
    try:
        # Décoder les données base64
        decoded_qr_data = base64.urlsafe_b64decode(qr_data).decode()
        
        # Analyser les données du QR code
        parts = decoded_qr_data.split(':')
        if len(parts) == 3 and parts[0] == 'ETUDIANT':
            matricule = parts[1]
            qr_code_data = parts[2]
            
            # Vérifier l'étudiant
            etudiant = get_object_or_404(
                Etudiant, 
                matricule=matricule, 
                qr_code_data=qr_code_data
            )
            
            return render(request, 'verify_qr.html', {
                'etudiant': etudiant,
                'is_valid': True
            })
        else:
            return render(request, 'verify_qr.html', {
                'is_valid': False,
                'error': 'Format de QR code invalide'
            })
    except Exception as e:
        return render(request, 'verify_qr.html', {
            'is_valid': False,
            'error': str(e)
        })