from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('ajouter_panier/<int:article_id>/', views.ajouter_panier, name='ajouter_panier'),
    path('panier/', views.panier, name='panier'),
    path('valider_commande/', views.valider_commande, name='valider_commande'),
    path('compte/', views.compte_client, name='compte_client'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Authentification
    path('login/', auth_views.LoginView.as_view(template_name='connexion.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='accueil'), name='logout'),
]
