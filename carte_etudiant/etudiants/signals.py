from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.conf import settings
from .models import Etudiant
import qrcode
from io import BytesIO
from django.core.files import File
import base64

@receiver(post_save, sender=Etudiant)
def generate_qr_code(sender, instance, created, **kwargs):
    if created or not instance.qr_code:
        # Générer les données du QR code
        qr_data = f"ETUDIANT:{instance.matricule}:{instance.qr_code_data}"
        
        # Encoder les données en base64 pour éviter les problèmes d'URL
        encoded_qr_data = base64.urlsafe_b64encode(qr_data.encode()).decode()
        
        # Créer l'URL absolue
        absolute_url = f"{settings.DOMAIN}{reverse('verify_qr', args=[encoded_qr_data])}"
        
        # Générer le QR code avec l'URL complète
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(absolute_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="#1e40af", back_color="white")
        
        # Sauvegarder l'image
        buffer = BytesIO()
        img.save(buffer, format='PNG')

        # --- C'EST LA LIGNE QU'IL FAUT AJOUTER ICI ---
        buffer.seek(0)
        
        # Nom du fichier
        file_name = f"qr_code_{instance.matricule}.png"
        
        # Sauvegarder le fichier
        instance.qr_code.save(file_name, File(buffer), save=False)
        instance.save()

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.urls import reverse
# from django.conf import settings
# from .models import Etudiant
# import qrcode
# from io import BytesIO
# from django.core.files import File
# import urllib.parse

# @receiver(post_save, sender=Etudiant)
# def generate_qr_code(sender, instance, created, **kwargs):
#     if created or not instance.qr_code:
#         # Générer les données du QR code
#         qr_data = f"ETUDIANT:{instance.matricule}:{instance.qr_code_data}"
        
#         # Encoder les données pour l'URL
#         encoded_qr_data = urllib.parse.quote(qr_data)
        
#         # Créer l'URL absolue
#         absolute_url = f"{settings.DOMAIN}{reverse('verify_qr', args=[encoded_qr_data])}"
        
#         # Générer le QR code avec l'URL complète
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#         )
#         qr.add_data(absolute_url)
#         qr.make(fit=True)
        
#         img = qr.make_image(fill_color="black", back_color="white")
        
#         # Sauvegarder l'image
#         buffer = BytesIO()
#         img.save(buffer, format='PNG')
        
#         # Nom du fichier
#         file_name = f"qr_code_{instance.matricule}.png"
        
#         # Sauvegarder le fichier
#         instance.qr_code.save(file_name, File(buffer), save=False)
#         instance.save()
        
        
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Etudiant
# import qrcode
# from io import BytesIO
# from django.core.files import File
# import os

# @receiver(post_save, sender=Etudiant)
# def generate_qr_code(sender, instance, created, **kwargs):
#     if created or not instance.qr_code:
#         # Données à encoder dans le QR code
#         qr_data = f"ETUDIANT:{instance.matricule}:{instance.qr_code_data}"
        
#         # Générer le QR code
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#         )
#         qr.add_data(qr_data)
#         qr.make(fit=True)
        
#         img = qr.make_image(fill_color="black", back_color="white")
        
#         # Sauvegarder l'image
#         buffer = BytesIO()
#         img.save(buffer, format='PNG')
        
#         # Nom du fichier
#         file_name = f"qr_code_{instance.matricule}.png"
        
#         # Sauvegarder le fichier
#         instance.qr_code.save(file_name, File(buffer), save=False)
#         instance.save()
