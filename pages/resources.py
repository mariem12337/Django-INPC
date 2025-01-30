from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import (
    Wilaya, Moughataa, Commune, ProductType, Product, PointOfSale, ProductPrice, Cart, CartProducts, Famille, Prix
)

# 1️⃣ Structures administratives
class WilayaResource(resources.ModelResource):
    class Meta:
        model = Wilaya
        fields = ('id', 'code', 'name')  # Champs à exporter/importer

class MoughataaResource(resources.ModelResource):
    wilaya = fields.Field(
        column_name='wilaya',
        attribute='wilaya',
        widget=ForeignKeyWidget(Wilaya, 'code')  # Utilisez 'code' comme identifiant
    )

    class Meta:
        model = Moughataa
        fields = ('id', 'code', 'label', 'wilaya')

class CommuneResource(resources.ModelResource):
    moughataa = fields.Field(
        column_name='moughataa',
        attribute='moughataa',
        widget=ForeignKeyWidget(Moughataa, 'code')  # Utilisez 'code' comme identifiant
    )

    class Meta:
        model = Commune
        fields = ('id', 'code', 'name', 'moughataa')

# 2️⃣ Produits et types de produits
class ProductTypeResource(resources.ModelResource):
    class Meta:
        model = ProductType
        fields = ('id', 'code', 'label', 'description')

class ProductResource(resources.ModelResource):
    product_type = fields.Field(
        column_name='product_type',
        attribute='product_type',
        widget=ForeignKeyWidget(ProductType, 'code')  # Utilisez 'code' comme identifiant
    )
    famille = fields.Field(
        column_name='famille',
        attribute='famille',
        widget=ForeignKeyWidget(Famille, 'nom')  # Utilisez 'nom' comme identifiant
    )

    class Meta:
        model = Product
        fields = ('id', 'code', 'name', 'description', 'unit_measure', 'product_type', 'famille')

# 3️⃣ Points de vente
class PointOfSaleResource(resources.ModelResource):
    commune = fields.Field(
        column_name='commune',
        attribute='commune',
        widget=ForeignKeyWidget(Commune, 'code')  # Utilisez 'code' comme identifiant
    )

    class Meta:
        model = PointOfSale
        fields = ('id', 'code', 'type', 'gps_lat', 'gps_lon', 'commune')

# 4️⃣ Prix des produits
class ProductPriceResource(resources.ModelResource):
    produit = fields.Field(
        column_name='produit',
        attribute='produit',
        widget=ForeignKeyWidget(Product, 'code')  # Utilisez 'code' comme identifiant
    )
    point_de_vente = fields.Field(
        column_name='point_de_vente',
        attribute='point_de_vente',
        widget=ForeignKeyWidget(PointOfSale, 'code')  # Utilisez 'code' comme identifiant
    )

    class Meta:
        model = ProductPrice
        fields = ('id', 'valeur', 'date_de_debut', 'date_fin', 'produit', 'point_de_vente')

# 5️⃣ Panier
class CartResource(resources.ModelResource):
    class Meta:
        model = Cart
        fields = ('id', 'code', 'name', 'description')

# Panier de produits
class CartProductsResource(resources.ModelResource):
    product = fields.Field(
        column_name='product',
        attribute='product',
        widget=ForeignKeyWidget(Product, 'code')  # Utilisez 'code' comme identifiant
    )
    cart = fields.Field(
        column_name='cart',
        attribute='cart',
        widget=ForeignKeyWidget(Cart, 'code')  # Utilisez 'code' comme identifiant
    )

    class Meta:
        model = CartProducts
        fields = ('id', 'product', 'cart', 'weight', 'date_from', 'date_to')

# 6️⃣ Famille de produits
class FamilleResource(resources.ModelResource):
    class Meta:
        model = Famille
        fields = ('id', 'nom', 'description')

# 7️⃣ Prix
class PrixResource(resources.ModelResource):
    produit = fields.Field(
        column_name='produit',
        attribute='produit',
        widget=ForeignKeyWidget(Product, 'code')  # Utilisez 'code' comme identifiant
    )

    class Meta:
        model = Prix
        fields = ('id', 'produit', 'prix', 'date')