from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Inventaire(models.Model):
    nom = models.CharField("Nom de l'article", max_length=30)
    description = models.CharField("Description de l'article", max_length=200)
    type = models.CharField("Type d'article", max_length=100)
    service = models.CharField("Service", max_length=50)
    piece = models.CharField("Pièce", max_length=50)
    derniere_commande = models.DateField("Dernière commande")
    fournisseur = models.CharField("Fournisseur", max_length=50)
    date_expiration_garantie = models.DateField("Fin de la garantie")
    condition = models.CharField("Condition de l'article", max_length=50)
    quantite = models.IntegerField("Quantité", default=1)
    prix = models.FloatField("Prix par item", default=0)

    def total(self):
        return self.quantite * self.prix

class Notes(models.Model):
    note = models.CharField("Note", max_length=250)
    date = models.DateTimeField("Date et heure", default=datetime.now())
    added_by = models.ForeignKey(User,
                                 null=True, blank=True, on_delete=models.SET_NULL)

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)