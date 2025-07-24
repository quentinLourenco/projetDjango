import os
import django
import random
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bonbonshop.settings") 
django.setup()

from boutique.models import Categorie, Article, Commande, LigneCommande
from django.contrib.auth.models import User
from django.utils import timezone

def run():
    print("🚀 Population de la base en cours...")

    # Catégories 
    noms_categories = [
        "Bonbons gélifiés", "Chocolats", "Sucettes", "Réglisse", "Bonbons acides",
        "Caramels", "Sans sucre", "Assortiments", "Confiseries vintage", "Bonbons de fête"
    ]

    categories = []
    for nom in noms_categories:
        c = Categorie.objects.create(nom=nom)
        categories.append(c)
    print("✅ Catégories créées.")

    # Articles 
    articles_data = [
        ("Ours Gélifiés", "Bonbons tendres multicolores", 2.50),
        ("Chocolat Noir 70%", "Carrés de chocolat noir intense", 3.90),
        ("Sucettes Fruitées", "Lot de 10 sucettes goût fraise", 1.80),
        ("Réglisse Douce", "Bâtons de réglisse naturelle", 2.20),
        ("Bonbons Citron Acide", "Petits bonbons piquants au citron", 2.00),
        ("Caramels Beurre Salé", "Caramels fondants au goût breton", 3.20),
        ("Bonbons Sans Sucre Menthe", "Idéal pour les diabétiques", 2.75),
        ("Mix Assortiment", "Mélange de 6 types de bonbons", 4.90),
        ("Boules Magiques", "Bonbons qui changent de goût !", 1.50),
        ("Guimauves Noël", "Bonbons en forme de sapin", 2.30),
    ]

    articles = []
    for i, (nom, desc, prix) in enumerate(articles_data):
        a = Article.objects.create(
            nom=nom,
            description=desc,
            prix=Decimal(prix),
            stock=random.randint(50, 200),
            categorie=categories[i % len(categories)]
        )
        articles.append(a)
    print("✅ Articles créés.")

    # Utilisateurs
    if not User.objects.filter(username="alice").exists():
        User.objects.create_user("alice", password="test123")
    if not User.objects.filter(username="bob").exists():
        User.objects.create_user("bob", password="test123")
    if not User.objects.filter(username="carla").exists():
        User.objects.create_user("carla", password="test123")

    users = list(User.objects.filter(username__in=["alice", "bob", "carla"]))

    # Commandes
    for _ in range(10):
        user = random.choice(users)
        commande = Commande.objects.create(
            client=user,
            validee=random.choice([True, False])
        )

        nb_articles = random.randint(1, 4)
        for _ in range(nb_articles):
            article = random.choice(articles)
            quantite = random.randint(1, 5)
            LigneCommande.objects.create(
                commande=commande,
                article=article,
                quantite=quantite
            )

    print("✅ Commandes et lignes de commandes créées.")
    print("🎉 Base de données initialisée avec succès !")

if __name__ == '__main__':
    run()
