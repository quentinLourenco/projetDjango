from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Categorie, Commande, LigneCommande
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum

from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Categorie
from django.contrib.auth.decorators import login_required

def accueil(request):
    categorie_id = request.GET.get('categorie')
    categories = Categorie.objects.all()
    articles = Article.objects.all()

    if categorie_id:
        articles = articles.filter(categorie_id=categorie_id)

    return render(request, 'accueil.html', {
        'categories': categories,
        'articles': articles
    })


def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'article_detail.html', {'article': article})

def ajouter_panier(request, article_id):
    if request.method == 'POST':
        quantite = int(request.POST.get('quantite', 1))
        panier = request.session.get('panier', {})
        panier[str(article_id)] = panier.get(str(article_id), 0) + quantite
        request.session['panier'] = panier
        return redirect('panier')

def panier(request):
    panier = request.session.get('panier', {})
    items = []
    total = 0

    for article_id, quantite in panier.items():
        article = Article.objects.get(id=article_id)
        total_ligne = article.prix * quantite
        items.append({
            'article': article,
            'quantite': quantite,
            'total': total_ligne,
        })
        total += total_ligne

    return render(request, 'panier.html', {'panier': items, 'total': total})

@login_required
def valider_commande(request):
    panier = request.session.get('panier', {})
    if not panier:
        return redirect('panier')

    total = 0
    commande = Commande.objects.create(client=request.user, total=0)

    for article_id, quantite in panier.items():
        article = Article.objects.get(id=article_id)
        total_ligne = article.prix * quantite
        LigneCommande.objects.create(commande=commande, article=article, quantite=quantite)
        total += total_ligne

    commande.total = total
    commande.validee = True
    commande.save()
    request.session['panier'] = {}

    return redirect('compte_client')


@login_required
def compte_client(request):
    commandes = Commande.objects.filter(client=request.user).order_by('-date_commande')
    return render(request, 'compte_client.html', {'commandes': commandes})


@staff_member_required
def dashboard(request):
    commandes = Commande.objects.filter(validee=True).order_by('-date_commande')
    ca_total = commandes.aggregate(Sum('total'))['total__sum'] or 0
    return render(request, 'admin/dashboard.html', {'commandes': commandes, 'ca_total': ca_total})