from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# IMPORTANT : Ajout du modèle Product et du ProductSerializer
from .models import Category, Product 
from .serializers import CategorySerializer, ProductSerializer 

def index(request):
    return HttpResponse('Bienvenu au pays mon fils')

# --- Vues existantes (inchangées) ---

class CategoryListAPIView(APIView):
    """
    API View pour afficher la liste des catégories actives
    """
    
    def get(self, request):
        try:
            # Récupérer seulement les catégories actives
            categories = Category.objects.filter(is_active=True).order_by('name')
            
            # Sérialiser les données
            serializer = CategorySerializer(categories, many=True)
            
            # Retourner la réponse
            return Response({
                'status': 'success',
                'message': 'Catégories récupérées avec succès',
                'count': categories.count(),
                'data': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Erreur lors de la récupération des catégories: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CategoryDetailAPIView(APIView):
    """
    API View pour afficher les détails d'une catégorie spécifique
    """
    
    def get(self, request, slug):
        try:
            # Récupérer la catégorie par son slug
            category = Category.objects.get(slug=slug, is_active=True)
            
            # Sérialiser les données
            serializer = CategorySerializer(category)
            
            return Response({
                'status': 'success',
                'message': 'Catégorie récupérée avec succès',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Category.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Catégorie non trouvée'
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Erreur lors de la récupération de la catégorie: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --- NOUVELLE VUE POUR LA CATÉGORIE ET SES PRODUITS ---

class CategoryProductsAPIView(APIView):
    """
    API View pour afficher les détails d'une catégorie et la liste de ses produits actifs.
    """

    def get(self, request, slug):
        try:
            # 1. Récupérer la catégorie par son slug
            category = Category.objects.get(slug=slug, is_active=True)
            
            # 2. Récupérer les produits actifs associés à cette catégorie
            # 'products' est le related_name défini dans models.py sur la clé étrangère Category
            products = category.products.filter(is_active=True).order_by('-created_at')
            
            # 3. Sérialiser la catégorie et les produits
            category_serializer = CategorySerializer(category)
            
            # *Passer le 'request' au contexte du ProductSerializer est essentiel 
            # pour obtenir l'URL complète des images.*
            product_serializer = ProductSerializer(
                products, 
                many=True, 
                context={'request': request}
            )
            
            # 4. Construire la réponse combinée
            return Response({
                'status': 'success',
                'message': f'Catégorie "{category.name}" et ses produits récupérés avec succès',
                'category_data': category_serializer.data,
                'products_count': products.count(),
                'products': product_serializer.data,
            }, status=status.HTTP_200_OK)
            
        except Category.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Catégorie non trouvée ou inactive'
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f"Erreur lors de la récupération de la catégorie et des produits: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)