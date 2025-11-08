from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category
from .serializers import CategorySerializer

def index(request):
    return HttpResponse('Bienvenu au pays mon fils')

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