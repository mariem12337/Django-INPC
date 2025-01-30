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


class MoughataaForm(forms.ModelForm):
    wilaya = forms.ModelChoiceField(queryset=Wilaya.objects.all(), required=True)  # ✅ Correction ici

    class Meta:
        model = Moughataa
        fields = ['code', 'label', 'wilaya']




class CommuneForm(forms.ModelForm):
    moughataa = forms.ModelChoiceField(
        queryset=Moughataa.objects.all(),
        required=True,
        label="Moughataa",
        widget=forms.Select(attrs={'class': 'form-control glowing-input'})  # Ajout d'un style Bootstrap
    )

    class Meta:
        model = Commune
        fields = ['code', 'name', 'moughataa']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control glowing-input'}),
            'name': forms.TextInput(attrs={'class': 'form-control glowing-input'}),
        }

class ProductForm(forms.ModelForm):
    product_type = forms.ModelChoiceField(
        queryset=ProductType.objects.all(),
        required=True,
        label="Type de Produit",
        widget=forms.Select(attrs={'class': 'form-control glowing-input'})
    )
    famille = forms.ModelChoiceField(
        queryset=Famille.objects.all(),
        required=True,
        label="Famille",
        widget=forms.Select(attrs={'class': 'form-control glowing-input'})
    )

    class Meta:
        model = Product
        fields = ['code', 'name', 'description', 'unit_measure', 'product_type', 'famille']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control glowing-input'}),
            'name': forms.TextInput(attrs={'class': 'form-control glowing-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control glowing-input'}),
            'unit_measure': forms.TextInput(attrs={'class': 'form-control glowing-input'}),
        }


# Formulaire pour ProductType
class ProductTypeForm(forms.ModelForm):
    class Meta:
        model = ProductType
        fields = ['code', 'label', 'description']



class PointOfSaleForm(forms.ModelForm):
    commune = forms.ModelChoiceField(
        queryset=Commune.objects.all(),
        required=True,
        label="Commune",
        widget=forms.Select(attrs={'class': 'form-control glowing-input'})
    )

    class Meta:
        model = PointOfSale
        fields = ['code', 'type', 'gps_lat', 'gps_lon', 'commune']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control glowing-input'}),
            'type': forms.TextInput(attrs={'class': 'form-control glowing-input'}),
            'gps_lat': forms.NumberInput(attrs={'class': 'form-control glowing-input', 'step': 'any'}),
            'gps_lon': forms.NumberInput(attrs={'class': 'form-control glowing-input', 'step': 'any'}),
        }




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






























