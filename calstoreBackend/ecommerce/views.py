from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# IMPORTANT : Ajout du modèle Product et du ProductSerializer
from .models import Category, Product, Customer, GuestCustomer, Address, Cart, Order, OrderItem
from rest_framework.permissions import AllowAny
from django.db import transaction
from rest_framework.status import HTTP_400_BAD_REQUEST 
from .serializers import (CategorySerializer, ProductSerializer, CategoryWithProductsSerializer) 

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
        
class CheckoutAPIView(APIView):
    """
    API View pour finaliser une commande (checkout)
    Gère à la fois les clients authentifiés et invités
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            data = request.data
            user = request.user
            
            # Vérifier les données requises
            required_fields = ['cart_id', 'payment_method', 'shipping_address', 'billing_address']
            for field in required_fields:
                if field not in data:
                    return Response({
                        'status': 'error',
                        'message': f'Le champ "{field}" est requis'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Commencer une transaction atomique
            with transaction.atomic():
                # 1. Récupérer ou créer le client
                customer, guest_customer = self._get_or_create_customer(user, data)
                
                # 2. Récupérer le panier
                cart = self._get_cart(data['cart_id'], customer, guest_customer)
                if not cart:
                    return Response({
                        'status': 'error',
                        'message': 'Panier non trouvé ou vide'
                    }, status=HTTP_400_BAD_REQUEST)
                
                # Vérifier si le panier est vide
                if cart.total_items == 0:
                    return Response({
                        'status': 'error',
                        'message': 'Le panier est vide'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # 3. Vérifier la disponibilité des produits
                availability_check = self._check_product_availability(cart)
                if not availability_check['available']:
                    return Response({
                        'status': 'error',
                        'message': 'Certains produits ne sont plus disponibles',
                        'unavailable_items': availability_check['unavailable_items']
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # 4. Créer ou récupérer les adresses
                billing_address = self._create_or_get_address(
                    data['billing_address'], 
                    'billing', 
                    customer, 
                    guest_customer
                )
                
                shipping_address = self._create_or_get_address(
                    data['shipping_address'], 
                    'shipping', 
                    customer, 
                    guest_customer
                )
                
                # 5. Calculer les prix
                price_calculation = self._calculate_prices(cart, data)
                
                # 6. Créer la commande
                order = self._create_order(
                    data=data,
                    customer=customer,
                    guest_customer=guest_customer,
                    billing_address=billing_address,
                    shipping_address=shipping_address,
                    price_calculation=price_calculation
                )
                
                # 7. Créer les items de commande
                order_items = self._create_order_items(order, cart)
                
                # 8. Vider le panier
                cart.items.all().delete()
                
                # 9. Mettre à jour les stocks
                self._update_inventory(cart)
                
                # 10. Préparer la réponse
                response_data = self._prepare_response(order, order_items)
                
                return Response({
                    'status': 'success',
                    'message': 'Commande créée avec succès',
                    'data': response_data
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Erreur lors du traitement de la commande: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _get_or_create_customer(self, user, data):
        """Récupérer ou créer un client (authentifié ou invité)"""
        customer = None
        guest_customer = None
        
        if user.is_authenticated:
            # Client authentifié
            customer = Customer.objects.filter(user=user).first()
            if not customer:
                # Créer un profil client si inexistant
                customer = Customer.objects.create(
                    user=user,
                    phone=data.get('phone', '')
                )
        else:
            # Client invité
            guest_email = data.get('guest_email')
            if not guest_email:
                raise ValueError("L'email est requis pour les clients invités")
            
            # Vérifier si un client invité existe déjà
            guest_customer = GuestCustomer.objects.filter(email=guest_email).first()
            if not guest_customer:
                # Créer un nouveau client invité
                guest_customer = GuestCustomer.objects.create(
                    email=guest_email,
                    first_name=data.get('guest_first_name', ''),
                    last_name=data.get('guest_last_name', ''),
                    phone=data.get('guest_phone', '')
                )
        
        return customer, guest_customer
    
    def _get_cart(self, cart_id, customer, guest_customer):
        """Récupérer le panier par ID, customer ou session"""
        try:
            # Essayer par UUID
            cart = Cart.objects.get(id=cart_id)
            
            # Vérifier l'appartenance
            if customer and cart.customer != customer:
                return None
            if guest_customer and cart.guest_customer != guest_customer:
                return None
            if not customer and not guest_customer and not cart.session_key:
                return None
                
            return cart
        except Cart.DoesNotExist:
            return None
    
    def _check_product_availability(self, cart):
        """Vérifier la disponibilité des produits dans le panier"""
        unavailable_items = []
        
        for cart_item in cart.items.all():
            product = cart_item.product
            variant = cart_item.variant
            
            if variant:
                # Vérifier la variante
                if variant.quantity < cart_item.quantity or not variant.is_active:
                    unavailable_items.append({
                        'product': product.name,
                        'variant': f"{variant.name}: {variant.value}",
                        'requested': cart_item.quantity,
                        'available': variant.quantity
                    })
            else:
                # Vérifier le produit principal
                if product.quantity < cart_item.quantity or not product.in_stock:
                    unavailable_items.append({
                        'product': product.name,
                        'requested': cart_item.quantity,
                        'available': product.quantity
                    })
        
        return {
            'available': len(unavailable_items) == 0,
            'unavailable_items': unavailable_items
        }
    
    def _create_or_get_address(self, address_data, address_type, customer, guest_customer):
        """Créer ou récupérer une adresse"""
        # Vérifier si une adresse par défaut existe déjà
        if customer:
            existing_address = Address.objects.filter(
                customer=customer,
                address_type=address_type,
                is_default=True
            ).first()
            if existing_address:
                return existing_address
        
        if guest_customer:
            existing_address = Address.objects.filter(
                guest_customer=guest_customer,
                address_type=address_type,
                is_default=True
            ).first()
            if existing_address:
                return existing_address
        
        # Créer une nouvelle adresse
        address = Address.objects.create(
            customer=customer,
            guest_customer=guest_customer,
            address_type=address_type,
            first_name=address_data.get('first_name', ''),
            last_name=address_data.get('last_name', ''),
            company=address_data.get('company', ''),
            address_line_1=address_data.get('address_line_1', ''),
            address_line_2=address_data.get('address_line_2', ''),
            city=address_data.get('city', ''),
            state=address_data.get('state', ''),
            postal_code=address_data.get('postal_code', ''),
            country=address_data.get('country', 'France'),
            phone=address_data.get('phone', ''),
            is_default=True
        )
        
        return address
    
    def _calculate_prices(self, cart, data):
        """Calculer les prix totaux de la commande"""
        subtotal = cart.subtotal
        
        # Calculer les frais de livraison (simplifié)
        shipping_price = 0
        if not data.get('is_digital', False):
            shipping_price = self._calculate_shipping(cart, data.get('shipping_method', 'standard'))
        
        # Calculer les taxes (simplifié - 20% pour la France)
        tax_rate = 0.20  # 20% de TVA
        tax_amount = subtotal * tax_rate
        
        # Appliquer les coupons (si fourni)
        discount_amount = 0
        coupon_code = data.get('coupon_code')
        if coupon_code:
            discount_amount = self._apply_coupon(cart, coupon_code)
        
        # Calculer le total
        total_price = subtotal + shipping_price + tax_amount - discount_amount
        
        return {
            'subtotal': subtotal,
            'shipping_price': shipping_price,
            'tax_amount': tax_amount,
            'discount_amount': discount_amount,
            'total_price': total_price
        }
    
    def _calculate_shipping(self, cart, shipping_method):
        """Calculer les frais de livraison (à adapter selon vos besoins)"""
        # Exemple simplifié
        shipping_methods = {
            'standard': 4.99,
            'express': 9.99,
            'free': 0
        }
        
        base_price = shipping_methods.get(shipping_method, 4.99)
        
        # Ajouter un supplément pour les produits lourds
        heavy_products = cart.items.filter(product__weight__gt=5)
        if heavy_products.exists():
            base_price += 5
        
        return base_price
    
    def _apply_coupon(self, cart, coupon_code):
        """Appliquer un coupon de réduction"""
        # Implémentation simplifiée - à compléter selon votre logique métier
        try:
            from .models import Coupon
            coupon = Coupon.objects.get(code=coupon_code, is_valid=True)
            
            if coupon.discount_type == 'percentage':
                discount = cart.subtotal * (coupon.discount_value / 100)
            else:
                discount = coupon.discount_value
            
            # Appliquer la limite maximale de réduction
            if coupon.maximum_discount and discount > coupon.maximum_discount:
                discount = coupon.maximum_discount
            
            # Vérifier le montant minimum
            if cart.subtotal < coupon.minimum_amount:
                return 0
            
            return discount
            
        except Coupon.DoesNotExist:
            return 0
    
    def _create_order(self, data, customer, guest_customer, billing_address, shipping_address, price_calculation):
        """Créer l'objet Order"""
        order = Order.objects.create(
            customer=customer,
            guest_customer=guest_customer,
            billing_address=billing_address,
            shipping_address=shipping_address,
            payment_method=data.get('payment_method', 'card'),
            shipping_method=data.get('shipping_method', 'standard'),
            subtotal=price_calculation['subtotal'],
            shipping_price=price_calculation['shipping_price'],
            tax_amount=price_calculation['tax_amount'],
            discount_amount=price_calculation['discount_amount'],
            total_price=price_calculation['total_price'],
            notes=data.get('notes', ''),
            ip_address=self._get_client_ip()
        )
        
        # Remplir les informations invité si nécessaire
        if guest_customer:
            order.guest_email = guest_customer.email
            order.guest_first_name = guest_customer.first_name
            order.guest_last_name = guest_customer.last_name
            order.guest_phone = guest_customer.phone
            order.save()
        
        return order
    
    def _get_client_ip(self):
        """Récupérer l'adresse IP du client"""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip
    
    def _create_order_items(self, order, cart):
        """Créer les OrderItems à partir du panier"""
        order_items = []
        
        for cart_item in cart.items.all():
            product = cart_item.product
            variant = cart_item.variant
            
            # Calculer le prix unitaire
            if variant:
                unit_price = product.price + variant.price_modifier
                sku = variant.sku or f"{product.sku}-{variant.name[:3]}-{variant.value[:3]}"
            else:
                unit_price = product.price
                sku = product.sku
            
            # Créer l'OrderItem
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                variant=variant,
                product_name=product.name,
                product_sku=sku,
                unit_price=unit_price,
                quantity=cart_item.quantity,
                total_price=unit_price * cart_item.quantity
            )
            
            order_items.append(order_item)
        
        return order_items
    
    def _update_inventory(self, cart):
        """Mettre à jour les stocks après la commande"""
        for cart_item in cart.items.all():
            product = cart_item.product
            variant = cart_item.variant
            
            if variant:
                # Mettre à jour le stock de la variante
                variant.quantity -= cart_item.quantity
                variant.save()
            
            # Mettre à jour le stock du produit principal
            product.quantity -= cart_item.quantity
            product.save()
    
    def _prepare_response(self, order, order_items):
        """Préparer les données de réponse"""
        # Sérialiser les produits pour la réponse
        order_items_data = []
        for item in order_items:
            product_data = ProductSerializer(item.product, context={'request': self.request}).data
            order_items_data.append({
                'id': item.id,
                'product': product_data,
                'variant': {
                    'name': item.variant.name if item.variant else None,
                    'value': item.variant.value if item.variant else None
                } if item.variant else None,
                'quantity': item.quantity,
                'unit_price': str(item.unit_price),
                'total_price': str(item.total_price)
            })
        
        return {
            'order': {
                'id': order.id,
                'order_number': order.order_number,
                'status': order.status,
                'payment_status': order.payment_status,
                'payment_method': order.payment_method,
                'subtotal': str(order.subtotal),
                'shipping_price': str(order.shipping_price),
                'tax_amount': str(order.tax_amount),
                'discount_amount': str(order.discount_amount),
                'total_price': str(order.total_price),
                'created_at': order.created_at,
                'billing_address': {
                    'first_name': order.billing_address.first_name,
                    'last_name': order.billing_address.last_name,
                    'address_line_1': order.billing_address.address_line_1,
                    'city': order.billing_address.city,
                    'postal_code': order.billing_address.postal_code,
                    'country': order.billing_address.country
                } if order.billing_address else None,
                'shipping_address': {
                    'first_name': order.shipping_address.first_name,
                    'last_name': order.shipping_address.last_name,
                    'address_line_1': order.shipping_address.address_line_1,
                    'city': order.shipping_address.city,
                    'postal_code': order.shipping_address.postal_code,
                    'country': order.shipping_address.country
                } if order.shipping_address else None
            },
            'order_items': order_items_data
        }