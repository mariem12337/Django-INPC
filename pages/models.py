# Create your models here.
from django.db import models

# 1️⃣ Structures administratives
class Wilaya(models.Model):
    code = models.CharField(max_length=10, unique=True)  # Augmenter la longueur à 10 caractères
    name = models.CharField(max_length=252)

    def __str__(self):
        return self.name



class Moughataa(models.Model):
    code = models.CharField(max_length=45)  
    label = models.CharField(max_length=45)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE)

    def __str__(self):
        return self.label  
    
   


class Commune(models.Model):
    code = models.CharField(max_length=45, unique=True)
    name = models.CharField(max_length=45)
    moughataa = models.ForeignKey(Moughataa, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# 2️⃣ Produits et types de produits
class ProductType(models.Model):
    code = models.CharField(max_length=45, unique=True)
    label = models.CharField(max_length=45)
    description = models.TextField()

    def __str__(self):
        return self.label



# Produits
class Product(models.Model):
    code = models.CharField(max_length=45, unique=True)
    name = models.CharField(max_length=45)
    description = models.TextField()
    unit_measure = models.CharField(max_length=45)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    famille = models.ForeignKey('Famille', on_delete=models.CASCADE)  # Added famille relation here

    def __str__(self):
        return self.name

# 3️⃣ Points de vente
class PointOfSale(models.Model):
    code = models.CharField(max_length=45, unique=True)
    type = models.CharField(max_length=45)
    gps_lat = models.FloatField()
    gps_lon = models.FloatField()
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)

    def __str__(self):
        return self.code

# 4️⃣ Prix des produits
class ProductPrice(models.Model):
    valeur = models.FloatField()
    date_de_debut = models.DateField()
    date_fin = models.DateField()
    produit = models.ForeignKey(Product, on_delete=models.CASCADE)  # En minuscules
    point_de_vente = models.ForeignKey(PointOfSale, on_delete=models.CASCADE)  # En minuscules
    
    def __str__(self):
        return f"{self.produit.name} - {self.valeur} ({self.date_de_debut} à {self.date_fin})"

# 5️⃣ Panier 
class Cart(models.Model):
    code = models.CharField(max_length=45, unique=True)
    name = models.CharField(max_length=45)
    description = models.TextField()

    def __str__(self):
        return self.name


# Panier de produits
class CartProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    weight = models.FloatField()
    date_from = models.DateField()
    date_to = models.DateField()

    def __str__(self):
        return f"{self.product.name} in {self.cart.name}"

# 6️⃣ Famille de produits
class Famille(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.nom

# 7️⃣ Prix
class Prix(models.Model):  # New model for product prices
    produit = models.ForeignKey(Product, on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.produit.name} - {self.prix} on {self.date}"



