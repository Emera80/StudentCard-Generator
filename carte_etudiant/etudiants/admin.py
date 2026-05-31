from django.contrib import admin
from .models import Faculte, Section, Promotion, Etudiant

# Register your models here.
admin.site.register(Faculte)
admin.site.register(Section)
admin.site.register(Promotion)
admin.site.register(Etudiant)