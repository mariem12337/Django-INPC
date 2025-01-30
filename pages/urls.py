from django.urls import path
from . import views

urlpatterns = [
    # Authentification
    path('connexion/', views.connexion, name='connexion'),
    path('accueil/', views.accueil, name='accueil'),


    # Gestion des Wilayas
    path('wilayas/', views.gestion_wilayas, name='gestion_wilayas'),

    # Gestion des Moughataas
    path('moughataas/', views.gestion_moughataas, name='gestion_moughataas'),

    # Gestion des Communes
    path('communes/', views.gestion_communes, name='gestion_communes'),

    # Gestion des Produits
    path('produits/', views.gestion_produits, name='gestion_produits'),

    # Gestion des Types de Produits
    path('product_types/', views.gestion_product_types, name='gestion_product_types'),

    # Gestion des Points de Vente
    path('points_de_vente/', views.gestion_points_de_vente, name='gestion_points_de_vente'),

    # Gestion des Prix des Produits
    path('product_prices/', views.gestion_product_prices, name='gestion_product_prices'),

    # Gestion des Paniers
    path('paniers/', views.gestion_paniers, name='gestion_paniers'),

    # Gestion des Produits dans les Paniers
    path('cart_products/', views.gestion_cart_products, name='gestion_cart_products'),

    # Gestion des Familles
    path('familles/', views.gestion_familles, name='gestion_familles'),

    # vue d'importation.
     path('import/', views.import_data, name='import_data'),
   
   
    # vue d'exportation. 
     path('export/', views.export_data, name='export_data'),
     
    
    # Page de calcul de l'INPC
    path('calculate_inpc/', views.calculate_inpc, name='calculate_inpc'),
    
    path('', views.home, name='home'),
    
]
