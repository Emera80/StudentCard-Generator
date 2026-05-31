from django.core import validators
from django.db import models
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

# Create your models here.
class Section(models.Model):
    ID_section = models.AutoField( primary_key = True)
    description_section = models.CharField( verbose_name="Section", max_length=50, unique=True)


    def __str__(self):
        return self.description_section
    
class Promotion(models.Model):
    ID_promotion = models.AutoField( primary_key = True)
    description_promotion = models.CharField(verbose_name="Promotion", max_length=50, unique=True)


    def __str__(self):
        return self.description_promotion
    
class Faculte(models.Model):
    ID_facule = models.AutoField( primary_key = True)
    description_faculte = models.CharField(verbose_name="Faculté", max_length=50, unique=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name= "facultes")

    def __str__(self):
        return f"{self.description_faculte} - {self.section.description_section}"

class Etudiant(models.Model):
    matricule = models.CharField(verbose_name="Matricule", max_length=10, unique=True , primary_key = True)
    nom_etudiant = models.CharField(verbose_name="Nom", max_length=50)
    prenom_etudiant = models.CharField(verbose_name="Prénom", max_length=50)
    postnom_etudiant = models.CharField(verbose_name="Postnom", max_length=50)
    # email = models.EmailField(verbose_name="Email", max_length=50, unique=True)
    sexe = models.CharField(verbose_name="Sexe", max_length=10, choices=[("M", "Masculin"), ("F", "Féminin")])
    date_naissance = models.DateField(verbose_name="Date de naissance", validators=[validators.MaxValueValidator(limit_value=datetime.date.today()), validators.MinValueValidator(limit_value=datetime.date(1900, 1, 1))])
    lieu_naissance = models.CharField(verbose_name="Lieu de naissance", max_length=120)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name= "etudiants")
    faculte = models.ForeignKey(Faculte, on_delete=models.CASCADE, related_name= "etudiants")
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    qr_code_data = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.matricule} - {self.nom_etudiant} {self.prenom_etudiant} {self.postnom_etudiant}"
    
    def infos_carte(self):
        return {
            "matricule": self.matricule,
            "nom_complet": f"{self.nom_etudiant} {self.postnom_etudiant or ''} {self.prenom_etudiant}".strip(),
            "promotion": self.promotion.nom,
            "faculte": self.promotion.section.faculte.nom,
            "sexe": self.get_sexe_display(),
            "date_naissance": self.date_naissance.strftime("%d/%m/%Y"),
            "lieu_naissance": self.lieu_naissance
        }   
        
    def save(self, *args, **kwargs):
        # Générer un identifiant unique pour le QR code si non existant
        if not self.qr_code_data:
            self.qr_code_data = str(uuid.uuid4())
        super().save(*args, **kwargs)



