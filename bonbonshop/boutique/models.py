from django.db import models
from django.contrib.auth.models import User

class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Article(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField()
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nom

class Commande(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    articles = models.ManyToManyField(Article, through='LigneCommande')
    date_commande = models.DateTimeField(auto_now_add=True)
    validee = models.BooleanField(default=False)

    def total(self):
        return sum(lc.article.prix * lc.quantite for lc in self.lignecommande_set.all())

class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
