# pages/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Wilaya, Moughataa, Commune, Product, ProductType, PointOfSale, ProductPrice, Cart, CartProducts, Famille
from .forms import WilayaForm, MoughataaForm, CommuneForm, ProductForm, ProductTypeForm, PointOfSaleForm, ProductPriceForm, CartForm, CartProductsForm, FamilleForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
import openpyxl
from datetime import datetime
from dateutil.relativedelta import relativedelta
# accueil

from django.shortcuts import render
from datetime import datetime
from .models import Product, ProductPrice, Cart, CartProducts

def calculate_inpc_for_date(date):
    """
    Calcule l'INPC pour une date donnée.
    """
    product_avg_prices = {}
    for product in Product.objects.all():
        avg_price = ProductPrice.objects.filter(
            product=product,
            date_from__lte=date,
            date_to__gte=date
        ).aggregate(Avg('value'))['value__avg']

        if avg_price is not None:
            product_avg_prices[product.id] = avg_price

    if not product_avg_prices:
        return 0  # Aucun prix disponible

    cart_inpc = {}
    for cart in Cart.objects.all():
        total_weighted_price = 0
        total_weight = 0

        cart_products = CartProducts.objects.filter(
            cart=cart,
            date_from__lte=date,
            date_to__gte=date
        )

        for cart_product in cart_products:
            product_id = cart_product.product.id
            if product_id in product_avg_prices:
                total_weighted_price += product_avg_prices[product_id] * cart_product.weight
                total_weight += cart_product.weight

        if total_weight > 0:
            cart_inpc[cart.id] = total_weighted_price / total_weight
        else:
            cart_inpc[cart.id] = 0

    if not cart_inpc:
        return 0

    return sum(cart_inpc.values()) / len(cart_inpc)
from django.contrib.auth.decorators import login_required


def accueil(request):
    aujourd_hui = datetime.now()
    inpc_data = []

    for i in range(4):
        mois = (aujourd_hui.month - i - 1) % 12 + 1
        annee = aujourd_hui.year if (aujourd_hui.month - i - 1) >= 0 else aujourd_hui.year - 1
        try:
            # Utilisation de calculate_inpc_for_date au lieu de calculer_inpc
            inpc = calculate_inpc_for_date(datetime(annee, mois, 1))
            inpc_data.append({
                'mois': mois,
                'annee': annee,
                'inpc': inpc
            })
        except Exception as e:
            inpc_data.append({
                'mois': mois,
                'annee': annee,
                'error': str(e)
            })

    context = {
        'inpc_data': inpc_data
    }
    return render(request, 'pages/accueil.html', context)


# connexion
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Connexion
def connexion(request):
    if request.method == 'POST':
        # Récupérer les champs du formulaire
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authentification de l'utilisateur
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Connexion réussie
            login(request, user)
            return redirect('accueil')  # Redirection vers la page d'accueil
        else:
            # Message d'erreur
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
            return render(request, 'pages/connexion.html')

    # Affichage du formulaire de connexion
    return render(request, 'pages/connexion.html')


# 1️⃣ Wilaya
def gestion_wilayas(request):
    wilayas = Wilaya.objects.all()
    form = WilayaForm(request.POST or None)
    wilaya = None

    if request.method == 'POST':
        if 'creer' in request.POST and form.is_valid():
            form.save()
            return redirect('gestion_wilayas')
        if 'modifier' in request.POST:
            wilaya_id = request.POST.get('wilaya_id')
            wilaya = get_object_or_404(Wilaya, id=wilaya_id)
            form = WilayaForm(request.POST, instance=wilaya)
            if form.is_valid():
                form.save()
                return redirect('gestion_wilayas')
        if 'supprimer' in request.POST:
            wilaya_id = request.POST.get('wilaya_id')
            wilaya = get_object_or_404(Wilaya, id=wilaya_id)
            wilaya.delete()
            return redirect('gestion_wilayas')

    return render(request, 'pages/gestion_wilayas.html', {'wilayas': wilayas, 'form': form, 'wilaya': wilaya})

# 2️⃣ Moughataa
def gestion_moughataas(request):
    moughataas = Moughataa.objects.all()  # Récupérer toutes les Moughataas
    wilayas = Wilaya.objects.all()  # Récupérer toutes les Wilayas
    form = MoughataaForm()

    if request.method == 'POST':
        print("Requête POST reçue:", request.POST)  # Debug pour voir le POST envoyé

        # 🔹 1. Création d'une nouvelle Moughataa
        if 'creer' in request.POST:
            form = MoughataaForm(request.POST)
            if form.is_valid():
                print("Formulaire valide, création en cours...")
                form.save()
                return redirect('gestion_moughataas')
            else:
                print("Formulaire invalide :", form.errors.as_json())

        # 🔹 2. Modification d'une Moughataa existante
        elif 'modifier' in request.POST:
            moughataa_id = request.POST.get('moughataa_id')
            moughataa = get_object_or_404(Moughataa, id=moughataa_id)
            form = MoughataaForm(request.POST, instance=moughataa)
            if form.is_valid():
                print("Modification enregistrée")
                form.save()
                return redirect('gestion_moughataas')
            else:
                print("Formulaire de modification invalide :", form.errors.as_json())

        # 🔹 3. Suppression d'une Moughataa
        elif 'supprimer' in request.POST:
            moughataa_id = request.POST.get('moughataa_id')  
            moughataa = get_object_or_404(Moughataa, id=moughataa_id)
            moughataa.delete()
            print(f"Moughataa {moughataa_id} supprimée avec succès")
            return redirect('gestion_moughataas')

    context = {
        'moughataas': moughataas,
        'wilayas': wilayas,
        'form': form,
    }
    return render(request, 'pages/gestion_moughataas.html', context)




def gestion_communes(request):
    communes = Commune.objects.all()  # Récupérer toutes les Communes
    moughataas = Moughataa.objects.all()  # Récupérer toutes les Moughataas
    form = CommuneForm()  # Formulaire vide par défaut
    commune = None  # Commune vide par défaut

    if request.method == 'POST':
        print("Requête POST reçue :", request.POST)  # Debugging
        
        # 🔹 Création d'une nouvelle Commune
        if 'creer' in request.POST:
            form = CommuneForm(request.POST)
            if form.is_valid():
                form.save()
                print("✅ Commune créée avec succès !")
                return redirect('gestion_communes')
            else:
                print("❌ Erreur de validation :", form.errors.as_json())

        # 🔹 Modification d'une Commune existante
        elif 'modifier' in request.POST:
            commune_id = request.POST.get('commune_id')
            commune = get_object_or_404(Commune, id=commune_id)
            form = CommuneForm(request.POST, instance=commune)
            if form.is_valid():
                form.save()
                print(f"✅ Commune {commune_id} modifiée avec succès !")
                return redirect('gestion_communes')
            else:
                print("❌ Erreur de modification :", form.errors.as_json())

        # 🔹 Suppression d'une Commune
        elif 'supprimer' in request.POST:
            commune_id = request.POST.get('commune_id')
            commune = get_object_or_404(Commune, id=commune_id)
            commune.delete()
            print(f"✅ Commune {commune_id} supprimée avec succès !")
            return redirect('gestion_communes')

    # 🔹 Contexte à passer au template
    context = {
        'communes': communes,
        'moughataas': moughataas,
        'form': form,
        'commune': commune  # Utilisé uniquement en cas de modification
    }
    return render(request, 'pages/gestion_communes.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, ProductType, Famille
from .forms import ProductForm

def gestion_produits(request):
    product_types = ProductType.objects.all()
    familles = Famille.objects.all()
    produits = Product.objects.all()
    form = ProductForm()
    produit = None  # Pour stocker un produit en cas de modification

    if request.method == 'POST':
        print("Requête POST reçue :", request.POST)  # Debugging

        # 🔹 Création d'un produit
        if 'creer' in request.POST:
            form = ProductForm(request.POST)
            if form.is_valid():
                form.save()
                print("✅ Produit créé avec succès !")
                return redirect('gestion_produits')
            else:
                print("❌ Erreur de validation :", form.errors.as_json())

        # 🔹 Modification d'un produit existant
        elif 'modifier' in request.POST:
            produit_id = request.POST.get('produit_id')
            produit = get_object_or_404(Product, id=produit_id)
            form = ProductForm(request.POST, instance=produit)
            if form.is_valid():
                form.save()
                print(f"✅ Produit {produit_id} modifié avec succès !")
                return redirect('gestion_produits')
            else:
                print("❌ Erreur de modification :", form.errors.as_json())

        # 🔹 Suppression d'un produit
        elif 'supprimer' in request.POST:
            produit_id = request.POST.get('produit_id')
            produit = get_object_or_404(Product, id=produit_id)
            produit.delete()
            print(f"✅ Produit {produit_id} supprimé avec succès !")
            return redirect('gestion_produits')

    context = {
        'produits': produits,
        'form': form,
        'produit': produit,
        'product_types': product_types,
        'familles': familles,
    }

    return render(request, 'pages/gestion_produits.html', context)


# ProductType (Types de produits)
from django.shortcuts import render, redirect, get_object_or_404
from .models import ProductType
from .forms import ProductTypeForm

def gestion_product_types(request):
    product_types = ProductType.objects.all()
    form = ProductTypeForm(request.POST or None)

    if request.method == 'POST':
        # Créer un type de produit
        if 'creer' in request.POST and form.is_valid():
            form.save()
            return redirect('gestion_product_types')

        # Modifier un type de produit
        if 'modifier' in request.POST:
            product_type_id = request.POST.get('edit_id')  # Récupérer l'ID à partir du champ caché
            product_type = get_object_or_404(ProductType, id=product_type_id)
            form = ProductTypeForm(request.POST, instance=product_type)
            if form.is_valid():
                form.save()
                return redirect('gestion_product_types')

        # Supprimer un type de produit
        if 'supprimer' in request.POST:
            product_type_id = request.POST.get('delete_id')
     
            product_type = get_object_or_404(ProductType, id=product_type_id)
            product_type.delete()
            return redirect('gestion_product_types')

    return render(request, 'pages/gestion_product_types.html', {'product_types': product_types, 'form': form})



def gestion_points_de_vente(request):
    points_de_vente = PointOfSale.objects.all()
    communes = Commune.objects.all()
    form = PointOfSaleForm()
    
    if request.method == 'POST':
        print("Requête POST reçue :", request.POST)  # Debugging
        
        # 🔹 Création d'un nouveau Point de Vente
        if 'creer' in request.POST:
            form = PointOfSaleForm(request.POST)
            if form.is_valid():
                form.save()
                print("✅ Point de Vente créé avec succès !")
                return redirect('gestion_points_de_vente')
            else:
                print("❌ Erreur de validation :", form.errors.as_json())

        # 🔹 Modification d'un Point de Vente existant
        elif 'modifier' in request.POST:
            point_id = request.POST.get('point_id')
            point = get_object_or_404(PointOfSale, id=point_id)
            form = PointOfSaleForm(request.POST, instance=point)
            if form.is_valid():
                form.save()
                print(f"✅ Point de Vente {point_id} modifié avec succès !")
                return redirect('gestion_points_de_vente')
            else:
                print("❌ Erreur de modification :", form.errors.as_json())

        # 🔹 Suppression d'un Point de Vente
        elif 'supprimer' in request.POST:
            point_id = request.POST.get('point_id')
            point = get_object_or_404(PointOfSale, id=point_id)
            point.delete()
            print(f"✅ Point de Vente {point_id} supprimé avec succès !")
            return redirect('gestion_points_de_vente')

    context = {
        'points_de_vente': points_de_vente,
        'communes': communes,
        'form': form
    }
    return render(request, 'pages/gestion_points_de_vente.html', context)


# ProductPrice (Prix des produits)

def gestion_product_prices(request):
    product_prices = ProductPrice.objects.all().select_related('produit', 'point_de_vente')
    form = ProductPriceForm(request.POST or None)

    if request.method == 'POST':
        if 'creer' in request.POST:
            if form.is_valid():
                form.save()
                messages.success(request, "Le prix a été ajouté avec succès.")
                print("Prix ajouté :", form.cleaned_data)  # Affiche les données insérées dans la console
                return redirect('gestion_product_prices')

        if 'modifier' in request.POST:
            product_price_id = request.POST.get('product_price_id')
            product_price = get_object_or_404(ProductPrice, id=product_price_id)
            form = ProductPriceForm(request.POST, instance=product_price)
            if form.is_valid():
                form.save()
                messages.success(request, "Le prix a été modifié avec succès.")
                return redirect('gestion_product_prices')

        if 'supprimer' in request.POST:
            product_price_id = request.POST.get('product_price_id')
            product_price = get_object_or_404(ProductPrice, id=product_price_id)
            product_price.delete()
            messages.success(request, "Le prix a été supprimé avec succès.")
            return redirect('gestion_product_prices')

    print("Prix récupérés :", product_prices)  # Affiche les données récupérées dans la console
    context = {
        'prix_produits': product_prices,
        'form': form,
        'produits': Product.objects.all(),
        'points_de_vente': PointOfSale.objects.all(),
    }
    return render(request, 'pages/gestion_product_prices.html', context)


# Cart (Panier de produits)
def gestion_paniers(request):
    paniers = Cart.objects.all()
    form = CartForm(request.POST or None)
    panier = None

    if request.method == 'POST':
        if 'creer' in request.POST and form.is_valid():
            form.save()
            return redirect('gestion_paniers')
        if 'modifier' in request.POST:
            panier_id = request.POST.get('panier_id')
            panier = get_object_or_404(Cart, id=panier_id)
            form = CartForm(request.POST, instance=panier)
            if form.is_valid():
                form.save()
                return redirect('gestion_paniers')
        if 'supprimer' in request.POST:
            panier_id = request.POST.get('panier_id')
            panier = get_object_or_404(Cart, id=panier_id)
            panier.delete()
            return redirect('gestion_paniers')

    return render(request, 'pages/gestion_paniers.html', {'paniers': paniers, 'form': form, 'panier': panier})


# CartProducts (Produits dans le panier)
def gestion_cart_products(request):
    cart_products = CartProducts.objects.all()
    form = CartProductsForm(request.POST or None)
    cart_product = None

    if request.method == 'POST':
        if 'creer' in request.POST and form.is_valid():
            form.save()
            return redirect('gestion_cart_products')
        if 'modifier' in request.POST:
            cart_product_id = request.POST.get('cart_product_id')
            cart_product = get_object_or_404(CartProducts, id=cart_product_id)
            form = CartProductsForm(request.POST, instance=cart_product)
            if form.is_valid():
                form.save()
                return redirect('gestion_cart_products')
        if 'supprimer' in request.POST:
            cart_product_id = request.POST.get('cart_product_id')
            cart_product = get_object_or_404(CartProducts, id=cart_product_id)
            cart_product.delete()
            return redirect('gestion_cart_products')

    return render(request, 'pages/gestion_cart_products.html', {'cart_products': cart_products, 'form': form, 'cart_product': cart_product})



# Famille 
def gestion_familles(request):
    familles = Famille.objects.all()
    form = FamilleForm(request.POST or None)

    if request.method == 'POST':
        if 'creer' in request.POST and form.is_valid():
            form.save()
            return redirect('gestion_familles')
        if 'modifier' in request.POST:
            famille_id = request.POST.get('edit_id')
            famille = get_object_or_404(Famille, id=famille_id)
            form = FamilleForm(request.POST, instance=famille)
            if form.is_valid():
                form.save()
                return redirect('gestion_familles')
        if 'supprimer' in request.POST:
            famille_id = request.POST.get('delete_id')
            famille = get_object_or_404(Famille, id=famille_id)
            famille.delete()
            return redirect('gestion_familles')

    return render(request, 'pages/gestion_familles.html', {'familles': familles, 'form': form})


### vue importer
from django.shortcuts import render, redirect
from django.contrib import messages
from .resources import (
    WilayaResource, MoughataaResource, CommuneResource, ProductResource,
    PointOfSaleResource, ProductPriceResource, CartResource, CartProductsResource,
    FamilleResource, PrixResource
)
from tablib import Dataset

def import_data(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        
        # Vérifier l'extension du fichier
        file_format = file.name.split('.')[-1].lower()
        if file_format not in ['csv', 'xlsx', 'xls']:
            messages.error(request, 'Format de fichier non supporté. Utilisez CSV ou Excel.')
            return redirect('import_data')

        dataset = Dataset()
        try:
            # Charger les données selon le format
            if file_format == 'csv':
                imported_data = dataset.load(file.read().decode('utf-8'), format='csv')
            else:
                imported_data = dataset.load(file.read(), format=file_format)

            # Récupérer le modèle sélectionné
            model_name = request.POST.get('model')

            # Dictionnaire de mapping des ressources
            resource_mapping = {
                'Wilaya': WilayaResource(),
                'Moughataa': MoughataaResource(),
                'Commune': CommuneResource(),
                'Product': ProductResource(),
                'PointOfSale': PointOfSaleResource(),
                'ProductPrice': ProductPriceResource(),
                'Cart': CartResource(),
                'CartProducts': CartProductsResource(),
                'Famille': FamilleResource(),
                'Prix': PrixResource()
            }

            resource = resource_mapping.get(model_name)

            if resource:
                try:
                    # Tester l'importation
                    result = resource.import_data(dataset, dry_run=True)
                    if not result.has_errors():
                        # Importer les données
                        resource.import_data(dataset, dry_run=False)
                        messages.success(request, "Données importées avec succès.")
                    else:
                        messages.error(request, f"Erreurs dans les données : {result.row_errors()}")
                except Exception as e:
                    messages.error(request, f"Erreur lors de l'importation : {str(e)}")
            else:
                messages.error(request, f"Modèle '{model_name}' non valide.")

        except Exception as e:
            messages.error(request, f"Erreur lors du traitement du fichier : {str(e)}")

        return redirect('import_data')

    return render(request, 'pages/import_data.html')

# Vue d'exportation
import csv
from django.http import HttpResponse
from .models import Wilaya, Moughataa, Commune, Product, PointOfSale, ProductPrice, Cart, CartProducts, Famille, Prix

def export_data(request):
    table = request.GET.get('table', None)

    valid_tables = {
        "Wilaya": Wilaya,
        "Moughataa": Moughataa,
        "Commune": Commune,
        "Product": Product,
        "PointOfSale": PointOfSale,
        "ProductPrice": ProductPrice,
        "Cart": Cart,
        "CartProducts": CartProducts,
        "Famille": Famille,
        "Prix": Prix,
    }

    if table not in valid_tables:
        return HttpResponse("Table non valide", status=400)

    model_class = valid_tables[table]

    # Récupération de tous les objets du modèle
    queryset = model_class.objects.all()

    # Créer la réponse CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{table}.csv"'

    # Exemple de création CSV : on récupère les champs dynamiquement
    writer = csv.writer(response)
    fields = [field.name for field in model_class._meta.get_fields()]

    # Écrire l’entête
    writer.writerow(fields)

    # Écrire les lignes de données
    for obj in queryset:
        row = []
        for field in fields:
            value = getattr(obj, field, "")
            row.append(value)
        writer.writerow(row)

    return response


## inpc: 

from django.shortcuts import render
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .utils import calculate_inpc_for_date

def calculate_inpc(request):
    if request.method == 'POST':
        try:
            mois = int(request.POST.get('mois'))
            annee = int(request.POST.get('annee'))

            if not 1 <= mois <= 12:
                raise ValueError("Le mois doit être entre 1 et 12.")

            date = datetime(annee, mois, 1).date()
            inpc = calculate_inpc_for_date(date)

            return render(request, 'pages/inpc_result.html', {
                'inpc': inpc,
                'month': mois,
                'year': annee
            })

        except Exception as e:
            return render(request, 'pages/calculate_inpc.html', {
                'error_message': f"Erreur : {str(e)}"
            })

    return render(request, 'pages/calculate_inpc.html')



## 
def home(request):
    inpc_data = []
    today = datetime.today()

    for i in range(4):
        # Calcul précis avec relativedelta
        date = today - relativedelta(months=i)
        inpc = calculate_inpc_for_date(date)
        
        inpc_data.append({
            'mois': date.month,
            'annee': date.year,
            'inpc': inpc
        })

    return render(request, 'pages/accueil.html', {'inpc_data': inpc_data})




