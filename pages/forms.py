from django import forms
from .models import Wilaya, Moughataa, Commune, Product, ProductType, PointOfSale, ProductPrice, Cart, CartProducts, Famille

# Formulaires pour chaque entité

# Connexion
class ConnexionForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre nom d\'utilisateur'})
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre mot de passe'})
    )


# Formulaire pour Wilaya
class WilayaForm(forms.ModelForm):
    class Meta:
        model = Wilaya
        fields = ['code', 'name']


# Formulaire pour Moughataa 
class MoughataaForm(forms.ModelForm):
    class Meta:
        model = Moughataa
        fields = ['code', 'label', 'wilaya']



# Formulaire pour Commune
class CommuneForm(forms.ModelForm):
    class Meta:
        model = Commune
        fields = ['code', 'name', 'moughataa']



# Formulaire pour Product
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


# Formulaire pour ProductType
class ProductTypeForm(forms.ModelForm):
    class Meta:
        model = ProductType
        fields = ['code', 'label', 'description']


# Formulaire pour PointOfSale
class PointOfSaleForm(forms.ModelForm):
    class Meta:
        model = PointOfSale
        fields = ['code', 'type', 'gps_lat', 'gps_lon', 'commune']



# Formulaire pour Prix(ProductPrice)
class ProductPriceForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_de_debut')
        date_fin = cleaned_data.get('date_fin')

        if date_debut and date_fin and date_debut > date_fin:
            raise forms.ValidationError("La date de début doit être antérieure à la date de fin.")
        return cleaned_data

    class Meta:
        model = ProductPrice
        fields = ['valeur', 'date_de_debut', 'date_fin', 'produit', 'point_de_vente']


# Formulaire pour Cart
class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['code', 'name', 'description']



# Formulaire pour CartProducts

class CartProductsForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')

        if date_from and date_to and date_from > date_to:
            raise forms.ValidationError("La date de début doit être antérieure à la date de fin.")
        return cleaned_data

    class Meta:
        model = CartProducts
        fields = '__all__'


# Formulaire pour Famille
class FamilleForm(forms.ModelForm):
    class Meta:
        model = Famille
        fields = ['nom', 'description']






























