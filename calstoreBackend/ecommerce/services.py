from django.db import transaction
from rest_framework.exceptions import ValidationError
from .models import Order, OrderItem, Address, Product, ProductVariant

from django.core.exceptions import ValidationError as DjangoValidationError
from .models import Cart, CartItem

class CartService:
    @staticmethod
    def get_or_create_cart(request):
        """
        Récupère ou crée un panier pour l'utilisateur connecté ou invité.
        """
        user = request.user
        
        # Utilisateur connecté
        if user.is_authenticated:
            customer = getattr(user, 'customer', None)
            if customer:
                cart, created = Cart.objects.get_or_create(customer=customer)
                return cart
        
        # Utilisateur invité : utilise la session
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        
        cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart

    @staticmethod
    @transaction.atomic
    def add_to_cart(cart, product_id, variant_id=None, quantity=1):
        """
        Ajoute un produit au panier ou met à jour la quantité.
        """
        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            raise ValidationError({"product": "Produit introuvable."})

        variant = None
        if variant_id:
            try:
                variant = ProductVariant.objects.get(id=variant_id, product=product, is_active=True)
            except ProductVariant.DoesNotExist:
                raise ValidationError({"variant": "Variante introuvable."})

        # Vérification du stock
        available_qty = variant.quantity if variant else product.quantity
        if quantity > available_qty:
            raise ValidationError({"quantity": f"Stock insuffisant. Disponible: {available_qty}"})

        # Mise à jour ou création
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={'quantity': quantity}
        )

        if not created:
            new_quantity = cart_item.quantity + quantity
            if new_quantity > available_qty:
                raise ValidationError({"quantity": f"Stock insuffisant. Disponible: {available_qty}"})
            cart_item.quantity = new_quantity
            cart_item.save()

        return cart_item

    @staticmethod
    @transaction.atomic
    def update_cart_item(cart_item, quantity):
        """
        Met à jour la quantité d'un item du panier.
        """
        product = cart_item.product
        variant = cart_item.variant

        available_qty = variant.quantity if variant else product.quantity
        
        if quantity > available_qty:
            raise ValidationError({"quantity": f"Stock insuffisant. Disponible: {available_qty}"})

        cart_item.quantity = quantity
        cart_item.save()
        return cart_item

    @staticmethod
    @transaction.atomic
    def remove_from_cart(cart_item):
        """
        Supprime un item du panier.
        """
        cart_item.delete()

    @staticmethod
    def clear_cart(cart):
        """
        Vide complètement le panier.
        """
        cart.items.all().delete()

class OrderService:
    @staticmethod
    @transaction.atomic
    def finalize_checkout(cart, validated_data):
        """
        Transforme un panier en commande ferme.
        """
        # 1. Vérification du panier
        if cart.items.count() == 0:
            raise ValidationError({"cart": "Le panier est vide."})

        # 2. Gestion des adresses
        # Ici on crée ou récupère les instances d'Address à partir des CharFields du serializer
        # (À adapter si vous préférez passer des IDs d'adresses pré-enregistrées)
        shipping_addr = Address.objects.create(
            customer=cart.customer,
            guest_customer=cart.guest_customer,
            address_type='shipping',
            address_line_1=validated_data['shipping_address'],
            # ... remplir les autres champs requis par votre modèle Address
        )
        
        billing_addr = Address.objects.create(
            customer=cart.customer,
            guest_customer=cart.guest_customer,
            address_type='billing',
            address_line_1=validated_data['billing_address'],
        )

        # 3. Création de la commande principale
        order = Order.objects.create(
            customer=cart.customer,
            guest_customer=cart.guest_customer,
            billing_address=billing_addr,
            shipping_address=shipping_addr,
            payment_method=validated_data['payment_method'],
            notes=validated_data.get('special_instructions', ''),
            subtotal=cart.subtotal,
            total_price=cart.total_price, # Le modèle calculera le numéro de commande au save()
            # Champs additionnels de votre nouveau serializer
            guest_email=validated_data.get('email', ''),
            guest_phone=validated_data.get('phone_number', '')
        )

        # 4. Création des OrderItems et gestion des stocks
        for item in cart.items.all():
            product = item.product
            variant = item.variant
            qty = item.quantity

            # Décrémentation du stock (Variante priorité sur Produit)
            if variant:
                if variant.quantity < qty:
                    raise ValidationError(f"Stock insuffisant pour {product.name} ({variant.value})")
                variant.quantity -= qty
                variant.save()
            else:
                if product.quantity < qty:
                    raise ValidationError(f"Stock insuffisant pour {product.name}")
                product.quantity -= qty
                product.save()

            # Snapshot de l'item
            OrderItem.objects.create(
                order=order,
                product=product,
                variant=variant,
                product_name=product.name,
                product_sku=variant.sku if variant else product.sku,
                unit_price=item.unit_price,
                quantity=qty,
                total_price=item.total_price
            )

        # 5. Nettoyage final
        cart.delete()
        
        return order