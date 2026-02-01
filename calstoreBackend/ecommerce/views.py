from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
import logging
# IMPORTANT : Ajout du modèle Product et du ProductSerializer
from .models import Category, Cart, CartItem
from .serializers import CheckoutSerializer, OrderSerializer
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST 
from .serializers import (
    CategorySerializer, ProductSerializer, 
    CategoryWithProductsSerializer, AddToCartSerializer, 
    UpdateCartItemSerializer, CartItemSerializer,
    CartSerializer, OrderSerializer, CheckoutSerializer
) 
from .services import (OrderService, CartService)

from .utils import send_order_telegram_notifications

logger = logging.getLogger(__name__)

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
            serializer = CategorySerializer(categories, many=True, context={'request': request})
            
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
        serializer = CheckoutSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            cart_id = serializer.validated_data['cart_id']
            cart = Cart.objects.get(id=cart_id)
            
            order = OrderService.finalize_checkout(
                cart=cart, 
                validated_data=serializer.validated_data
            )
            
            # Sérialisation de la commande
            order_serializer = OrderSerializer(order)
            order_data = order_serializer.data
            
            # Préparation des données pour la notification
            notification_data = self._prepare_notification_data(order, order_data)
            
            # Envoi de la notification (optionnel, peut échouer sans bloquer)
            try:
                send_order_telegram_notifications(**notification_data)
            except Exception as e:
                # Log l'erreur mais ne fais pas échouer la commande
                logger.error(f"Notification Telegram échouée pour la commande {order.id}: {e}")
            
            return Response(order_data, status=status.HTTP_201_CREATED)
            
        except Cart.DoesNotExist:
            return Response({"error": "Panier introuvable"}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"error": e.detail if hasattr(e, 'detail') else str(e)}, 
                          status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(f"Erreur lors du checkout: {e}")
            return Response({"error": "Erreur interne du serveur"}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _prepare_notification_data(self, order, order_data):
        """Prépare les données pour la notification Telegram"""
        # Récupération du nom du client
        customer_name = self._extract_customer_name(order, order_data)
        
        # Récupération des articles
        items = self._extract_items(order_data)
        
        return {
            'id': order.id,
            'order_number': order_data.get('order_number', f"CMD-{order.id}"),
            'customer': customer_name,
            'items': items,
            'total_price': order_data.get('total_price', 0)
        }
    
    def _extract_customer_name(self, order, order_data):
        """Extrait le nom du client depuis l'order ou les données sérialisées"""
        # Essayer depuis l'order d'abord
        if order.customer:
            return order.customer.get_full_name()
        elif order.guest_email:
            return f"Client ({order.guest_email})"
        
        # Fallback sur les données sérialisées
        customer_data = order_data.get('customer')
        if isinstance(customer_data, dict):
            return customer_data.get('name', 'Client')
        
        return order_data.get('customer_name', 'Client')
    
    def _extract_items(self, order_data):
        """Extrait la liste des articles formatés"""
        items = order_data.get('items', [])
        if not items:
            return []
        
        # Format minimal pour Telegram
        return [
            {
                'name': item.get('product_name', item.get('name', 'Produit'))[:50],
                'quantity': item.get('quantity', 1)
            }
            for item in items[:10]  # Limite à 10 articles max
        ]