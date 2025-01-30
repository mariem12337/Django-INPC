from django.db.models import Avg, Sum
from .models import Product, ProductPrice, Cart, CartProducts

def calculate_inpc_for_date(date):
    """
    Calcule l'INPC pour une date donnée.
    """
    # Étape 1 : Calculer le prix moyen de chaque produit pour la date donnée
    product_avg_prices = (
        ProductPrice.objects
        .filter(date_de_debut__lte=date, date_fin__gte=date)
        .values('produit')
        .annotate(avg_price=Avg('valeur'))
    )

    # Convertir en dictionnaire pour un accès rapide
    product_avg_prices = {item['produit']: item['avg_price'] for item in product_avg_prices}

    # Si aucun prix n'est disponible, retourner 0
    if not product_avg_prices:
        return 0

    # Étape 2 : Calculer l'INPC pour chaque panier
    cart_inpc = []
    for cart in Cart.objects.all():
        # Récupérer les produits du panier valides à la date donnée
        cart_products = (
            CartProducts.objects
            .filter(cart=cart, date_from__lte=date, date_to__gte=date)
            .select_related('product')
        )

        # Calculer le prix pondéré pour chaque produit dans le panier
        total_weighted_price = 0
        total_weight = 0

        for cart_product in cart_products:
            product_id = cart_product.product.id
            if product_id in product_avg_prices:
                total_weighted_price += product_avg_prices[product_id] * cart_product.weight
                total_weight += cart_product.weight

        # Calculer l'INPC pour ce panier
        if total_weight > 0:
            cart_inpc.append(total_weighted_price / total_weight)

    # Si aucun panier n'est disponible, retourner 0
    if not cart_inpc:
        return 0

    # Étape 3 : Calculer l'INPC global (moyenne des INPC des paniers)
    return sum(cart_inpc) / len(cart_inpc)
