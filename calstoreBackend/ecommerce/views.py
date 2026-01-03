from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

# IMPORTANT : Ajout du modèle Product et du ProductSerializer
from .models import Category, Cart, CartItem
from .serializers import CheckoutSerializer, OrderSerializer
from rest_framework.permissions import AllowAny
from django.db import transaction
from rest_framework.status import HTTP_400_BAD_REQUEST 
from .serializers import (
    CategorySerializer, ProductSerializer, 
    CategoryWithProductsSerializer, AddToCartSerializer, 
    UpdateCartItemSerializer, CartItemSerializer,
    CartSerializer, OrderSerializer, CheckoutSerializer
) 
from .services import (OrderService, CartService)

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
            serializer = CategoryWithProductsSerializer(categories, many=True, context={'request': request})
            
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
    Inclut les produits si le paramètre with_products est présent
    """
    
    def get(self, request, slug):
        try:
            # Récupérer la catégorie par son slug
            category = Category.objects.get(slug=slug, is_active=True)
            
            # Vérifier si on veut aussi les produits
            with_products = request.query_params.get('with_products', 'false').lower() == 'true'
            
            if with_products:
                # Récupérer les produits actifs associés
                products = category.products.filter(is_active=True).order_by('-created_at')
                
                # Sérialiser avec les produits
                serializer = CategoryWithProductsSerializer(category, context={'request': request})
                
                response_data = {
                    'status': 'success',
                    'message': f'Catégorie "{category.name}" et ses produits récupérés avec succès',
                    'data': serializer.data,
                    'products_count': products.count()
                }
            else:
                # Sérialiser seulement la catégorie
                serializer = CategorySerializer(category, context={'request': request})
                
                response_data = {
                    'status': 'success',
                    'message': 'Catégorie récupérée avec succès',
                    'data': serializer.data
                }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
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

class CartAPIView(APIView):
    """
    GET: Récupère le panier actuel
    DELETE: Vide le panier
    """
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            cart = CartService.get_or_create_cart(request)
            serializer = CartSerializer(cart, context={'request': request})
            
            return Response({
                'status': 'success',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        """Vider le panier"""
        try:
            cart = CartService.get_or_create_cart(request)
            CartService.clear_cart(cart)
            
            return Response({
                'status': 'success',
                'message': 'Panier vidé avec succès'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class AddToCartAPIView(APIView):
    """
    POST: Ajoute un produit au panier
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = CartService.get_or_create_cart(request)
            cart_item = CartService.add_to_cart(
                cart=cart,
                product_id=serializer.validated_data['product_id'],
                variant_id=serializer.validated_data.get('variant_id'),
                quantity=serializer.validated_data.get('quantity', 1)
            )

            return Response({
                'status': 'success',
                'message': 'Produit ajouté au panier',
                'data': CartItemSerializer(cart_item, context={'request': request}).data
            }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({
                'status': 'error',
                'errors': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)


class CartItemAPIView(APIView):
    """
    PATCH: Modifier la quantité d'un item
    DELETE: Supprimer un item du panier
    """
    permission_classes = [AllowAny]

    def patch(self, request, item_id):
        serializer = UpdateCartItemSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = CartService.get_or_create_cart(request)
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            
            updated_item = CartService.update_cart_item(
                cart_item=cart_item,
                quantity=serializer.validated_data['quantity']
            )

            return Response({
                'status': 'success',
                'message': 'Quantité mise à jour',
                'data': CartItemSerializer(updated_item, context={'request': request}).data
            }, status=status.HTTP_200_OK)

        except CartItem.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Item non trouvé dans le panier'
            }, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({
                'status': 'error',
                'errors': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_id):
        try:
            cart = CartService.get_or_create_cart(request)
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            
            CartService.remove_from_cart(cart_item)

            return Response({
                'status': 'success',
                'message': 'Produit retiré du panier'
            }, status=status.HTTP_200_OK)

        except CartItem.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Item non trouvé'
            }, status=status.HTTP_404_NOT_FOUND)

class CheckoutAPIView(APIView):
    def post(self, request):
        # Initialisation du serializer avec les données JSON
        serializer = CheckoutSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                # Récupération du panier validé par le serializer
                cart_id = serializer.validated_data['cart_id']
                cart = Cart.objects.get(id=cart_id)

                # Appel au service pour la logique métier
                order = OrderService.finalize_checkout(
                    cart=cart, 
                    validated_data=serializer.validated_data
                )

                # Réponse avec le détail de la commande créée
                response_serializer = OrderSerializer(order)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)

            except Cart.DoesNotExist:
                return Response({"error": "Panier introuvable"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)