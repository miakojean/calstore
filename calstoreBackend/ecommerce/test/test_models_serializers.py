# tests/test_models_and_serializers.py
import uuid
from decimal import Decimal
from datetime import datetime, timedelta
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request

from ..models import (
    Category, Brand, Product, ProductImage, ProductVariant,
    GuestCustomer, Customer, Address, Cart, CartItem,
    Order, OrderItem, Review, Wishlist, Coupon, Payment
)
from ..serializers import (
    BrandSerializer, ProductImageSerializer, ProductVariantSerializer,
    ProductSerializer, CategorySerializer, CategoryWithProductsSerializer,
    CartItemSerializer, CartSerializer, AddToCartSerializer,
    UpdateCartItemSerializer, OrderItemSerializer, OrderSerializer,
    CheckoutSerializer
)


class ModelTests(TestCase):
    """Tests pour les modèles"""

    @classmethod
    def setUpTestData(cls):
        # Création d'une catégorie
        cls.category = Category.objects.create(
            name="Electronics",
            slug="electronics",
            description="Electronic items"
        )
        # Création d'une marque
        cls.brand = Brand.objects.create(
            name="Samsung",
            slug="samsung"
        )
        # Création d'un produit
        cls.product = Product.objects.create(
            name="Galaxy S21",
            slug="galaxy-s21",
            description="Latest smartphone",
            price=Decimal("799.00"),
            compare_price=Decimal("899.00"),
            quantity=15,
            category=cls.category,
            brand=cls.brand,
            sku="S21-BLK-128"
        )
        # Image principale
        cls.main_image = ProductImage.objects.create(
            product=cls.product,
            image=SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg"),
            is_main=True,
            order=1
        )
        # Variante
        cls.variant = ProductVariant.objects.create(
            product=cls.product,
            name="Color",
            value="Black",
            price_modifier=Decimal("0.00"),
            quantity=5
        )
        # Client invité
        cls.guest = GuestCustomer.objects.create(
            email="guest@example.com",
            first_name="John",
            last_name="Doe",
            phone="+123456789",
            agree_terms=True
        )
        # Client enregistré
        cls.user = User.objects.create_user(
            username="john_doe",
            email="john@example.com",
            password="testpass123"
        )
        cls.customer = Customer.objects.create(
            user=cls.user,
            phone="+987654321",
            newsletter_subscription=True
        )
        # Adresse
        cls.address = Address.objects.create(
            customer=cls.customer,
            address_type="shipping",
            first_name="John",
            last_name="Doe",
            address_line_1="123 Main St",
            city="Paris",
            state="IDF",
            postal_code="75001",
            country="France",
            is_default=True
        )
        # Panier
        cls.cart = Cart.objects.create(
            customer=cls.customer,
            session_key="test_session"
        )
        cls.cart_item = CartItem.objects.create(
            cart=cls.cart,
            product=cls.product,
            variant=cls.variant,
            quantity=2
        )
        # Commande
        cls.order = Order.objects.create(
            order_number="ORD-TEST123",
            customer=cls.customer,
            subtotal=Decimal("1598.00"),
            shipping_price=Decimal("10.00"),
            tax_amount=Decimal("0.00"),
            discount_amount=Decimal("0.00"),
            total_price=Decimal("1608.00"),
            billing_address=cls.address,
            shipping_address=cls.address
        )
        cls.order_item = OrderItem.objects.create(
            order=cls.order,
            product=cls.product,
            variant=cls.variant,
            product_name=cls.product.name,
            product_sku=cls.product.sku,
            unit_price=cls.product.price,
            quantity=1,
            total_price=cls.product.price
        )

    # --- Tests Category ---
    def test_category_str(self):
        self.assertEqual(str(self.category), "Electronics")

    def test_category_ordering(self):
        cat2 = Category.objects.create(name="Books", slug="books")
        categories = list(Category.objects.all())
        self.assertEqual(categories[0].name, "Books")  # ordre alphabétique
        self.assertEqual(categories[1].name, "Electronics")

    # --- Tests Brand ---
    def test_brand_str(self):
        self.assertEqual(str(self.brand), "Samsung")

    # --- Tests Product ---
    def test_product_in_stock(self):
        self.assertTrue(self.product.in_stock)
        self.product.quantity = 0
        self.product.save()
        self.assertFalse(self.product.in_stock)

    def test_product_is_on_sale(self):
        self.assertTrue(self.product.is_on_sale)
        self.product.compare_price = None
        self.product.save()
        self.assertFalse(self.product.is_on_sale)

    def test_product_discount_percentage(self):
        self.assertEqual(self.product.discount_percentage, 11)  # (899-799)/899*100 ≈ 11%
        self.product.compare_price = Decimal("1000.00")
        self.product.save()
        self.assertEqual(self.product.discount_percentage, 20)

    def test_product_main_image(self):
        self.assertEqual(self.product.main_image, self.main_image)

    # --- Tests ProductImage ---
    def test_product_image_str(self):
        self.assertIn("Galaxy S21", str(self.main_image))

    def test_product_image_ordering(self):
        img2 = ProductImage.objects.create(product=self.product, order=0, image=SimpleUploadedFile("test2.jpg", b"content"))
        images = list(ProductImage.objects.filter(product=self.product))
        self.assertEqual(images[0].order, 0)  # order puis created_at
        self.assertEqual(images[1].order, 1)

    # --- Tests ProductVariant ---
    def test_product_variant_str(self):
        self.assertEqual(str(self.variant), "Galaxy S21 - Color: Black")

    def test_product_variant_unique_together(self):
        with self.assertRaises(Exception):
            ProductVariant.objects.create(
                product=self.product,
                name="Color",
                value="Black"
            )

    # --- Tests GuestCustomer ---
    def test_guest_customer_str(self):
        self.assertEqual(str(self.guest), "John Doe (guest@example.com)")

    # --- Tests Customer ---
    def test_customer_str(self):
        self.assertEqual(str(self.customer), "john_doe")

    # --- Tests Address ---
    def test_address_clean_requires_customer_or_guest(self):
        address = Address(
            address_type="billing",
            first_name="Alone",
            last_name="Walker",
            address_line_1="No customer"
        )
        with self.assertRaises(ValidationError):
            address.clean()

    def test_address_str(self):
        self.assertEqual(str(self.address), "Shipping - Paris, France")

    # --- Tests Cart ---
    def test_cart_total_items(self):
        self.assertEqual(self.cart.total_items, 2)

    def test_cart_subtotal(self):
        expected = self.cart_item.unit_price * 2
        self.assertEqual(self.cart.subtotal, expected)

    def test_cart_total_price(self):
        self.assertEqual(self.cart.total_price, self.cart.subtotal)

    # --- Tests CartItem ---
    def test_cartitem_unit_price_with_variant(self):
        self.assertEqual(self.cart_item.unit_price, self.product.price + self.variant.price_modifier)

    def test_cartitem_unit_price_without_variant(self):
        item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        self.assertEqual(item.unit_price, self.product.price)

    def test_cartitem_total_price(self):
        expected = self.cart_item.unit_price * self.cart_item.quantity
        self.assertEqual(self.cart_item.total_price, expected)

    def test_cartitem_unique_together(self):
        with self.assertRaises(Exception):
            CartItem.objects.create(
                cart=self.cart,
                product=self.product,
                variant=self.variant,
                quantity=1
            )

    # --- Tests Order ---
    def test_order_generate_order_number(self):
        order = Order.objects.create(
            customer=self.customer,
            subtotal=Decimal("100.00"),
            total_price=Decimal("100.00")
        )
        self.assertTrue(order.order_number.startswith("ORD-"))
        self.assertEqual(len(order.order_number), 14)  # ORD- + 10 chars

    def test_order_save_populates_guest_fields(self):
        guest_order = Order.objects.create(
            guest_customer=self.guest,
            subtotal=Decimal("50.00"),
            total_price=Decimal("50.00")
        )
        self.assertEqual(guest_order.guest_email, self.guest.email)
        self.assertEqual(guest_order.guest_first_name, self.guest.first_name)

    def test_order_customer_name_property(self):
        self.assertEqual(self.order.customer_name, str(self.customer))
        # Pour une commande guest
        guest_order = Order.objects.create(
            guest_customer=self.guest,
            subtotal=Decimal("50.00"),
            total_price=Decimal("50.00")
        )
        self.assertEqual(guest_order.customer_name, str(self.guest))

    def test_order_customer_email_property(self):
        self.assertEqual(self.order.customer_email, self.user.email)
        guest_order = Order.objects.create(
            guest_customer=self.guest,
            subtotal=Decimal("50.00"),
            total_price=Decimal("50.00")
        )
        self.assertEqual(guest_order.customer_email, self.guest.email)

    # --- Tests OrderItem ---
    def test_order_item_str(self):
        self.assertEqual(str(self.order_item), f"1 x {self.product.name}")

    # --- Tests Review ---
    def test_review_unique_together(self):
        Review.objects.create(
            product=self.product,
            customer=self.customer,
            rating=5,
            title="Great",
            comment="Awesome"
        )
        with self.assertRaises(Exception):
            Review.objects.create(
                product=self.product,
                customer=self.customer,
                rating=4,
                title="Also great",
                comment="Still good"
            )

    # --- Tests Wishlist ---
    def test_wishlist_str(self):
        wishlist = Wishlist.objects.create(customer=self.customer)
        self.assertEqual(str(wishlist), f"Wishlist of {self.customer}")

    # --- Tests Coupon ---
    def test_coupon_is_valid(self):
        now = timezone.now()
        valid_coupon = Coupon.objects.create(
            code="VALID20",
            discount_type="percentage",
            discount_value=20,
            valid_from=now - timedelta(days=1),
            valid_until=now + timedelta(days=1),
            is_active=True
        )
        self.assertTrue(valid_coupon.is_valid)

        expired_coupon = Coupon.objects.create(
            code="EXPIRED",
            discount_type="percentage",
            discount_value=10,
            valid_from=now - timedelta(days=2),
            valid_until=now - timedelta(days=1),
            is_active=True
        )
        self.assertFalse(expired_coupon.is_valid)

    # --- Tests Payment ---
    def test_payment_str(self):
        payment = Payment.objects.create(
            order=self.order,
            payment_method="card",
            payment_gateway="stripe",
            transaction_id="txn_123",
            amount=self.order.total_price,
            status="completed"
        )
        self.assertIn("txn_123", str(payment))
        self.assertIn(self.order.order_number, str(payment))


class SerializerTests(TestCase):
    """Tests pour les sérialiseurs"""

    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
        cls.request = Request(cls.factory.get("/"))
        cls.category = Category.objects.create(
            name="Electronics",
            slug="electronics",
            description="Gadgets"
        )
        cls.brand = Brand.objects.create(name="Sony", slug="sony")
        cls.product = Product.objects.create(
            name="Headphones",
            slug="headphones",
            description="Noise cancelling",
            price=Decimal("199.99"),
            compare_price=Decimal("249.99"),
            quantity=10,
            category=cls.category,
            brand=cls.brand,
            sku="HP-100"
        )
        cls.main_image = ProductImage.objects.create(
            product=cls.product,
            image=SimpleUploadedFile("test.jpg", b"img", content_type="image/jpeg"),
            is_main=True
        )
        cls.variant = ProductVariant.objects.create(
            product=cls.product,
            name="Color",
            value="Black",
            price_modifier=Decimal("0.00"),
            quantity=3
        )
        cls.user = User.objects.create_user(username="buyer", password="pass")
        cls.customer = Customer.objects.create(user=cls.user)
        cls.cart = Cart.objects.create(customer=cls.customer)
        cls.cart_item = CartItem.objects.create(
            cart=cls.cart,
            product=cls.product,
            variant=cls.variant,
            quantity=2
        )

    # --- BrandSerializer ---
    def test_brand_serializer(self):
        serializer = BrandSerializer(self.brand)
        data = serializer.data
        self.assertEqual(data["name"], "Sony")
        self.assertEqual(data["slug"], "sony")
        self.assertIn("logo", data)

    # --- ProductImageSerializer ---
    def test_product_image_serializer(self):
        serializer = ProductImageSerializer(self.main_image)
        data = serializer.data
        self.assertEqual(data["is_main"], True)
        self.assertEqual(data["order"], 0)
        self.assertIn("image", data)

    # --- ProductVariantSerializer ---
    def test_product_variant_serializer(self):
        serializer = ProductVariantSerializer(self.variant)
        data = serializer.data
        self.assertEqual(data["name"], "Color")
        self.assertEqual(data["value"], "Black")
        self.assertEqual(Decimal(data["price_modifier"]), Decimal("0.00"))

    # --- ProductSerializer ---
    def test_product_serializer_fields(self):
        serializer = ProductSerializer(self.product, context={"request": self.request})
        data = serializer.data
        self.assertEqual(data["name"], "Headphones")
        self.assertEqual(Decimal(data["price"]), Decimal("199.99"))
        self.assertTrue(data["is_on_sale"])
        self.assertEqual(data["discount_percentage"], 20)  # (249.99-199.99)/249.99*100 ≈ 20
        self.assertTrue(data["in_stock"])
        self.assertIsNotNone(data["main_image"])
        self.assertIn("main_image_url", data)
        self.assertIn("images", data)
        self.assertIn("variants", data)
        self.assertEqual(data["category"], "Electronics")  # StringRelatedField

    def test_product_serializer_main_image_url(self):
        serializer = ProductSerializer(self.product, context={"request": self.request})
        url = serializer.data["main_image_url"]
        self.assertIsNotNone(url)
        self.assertTrue(url.startswith("http"))

    # --- CategorySerializer ---
    def test_category_serializer(self):
        serializer = CategorySerializer(self.category, context={"request": self.request})
        data = serializer.data
        self.assertEqual(data["name"], "Electronics")
        self.assertIn("image_url", data)

    # --- CategoryWithProductsSerializer ---
    def test_category_with_products_serializer(self):
        serializer = CategoryWithProductsSerializer(self.category, context={"request": self.request})
        data = serializer.data
        self.assertEqual(data["name"], "Electronics")
        self.assertIn("products", data)
        self.assertEqual(len(data["products"]), 1)
        self.assertEqual(data["products"][0]["name"], "Headphones")

    # --- CartItemSerializer ---
    def test_cart_item_serializer_read(self):
        serializer = CartItemSerializer(self.cart_item)
        data = serializer.data
        self.assertEqual(data["quantity"], 2)
        self.assertEqual(Decimal(data["unit_price"]), self.product.price + self.variant.price_modifier)
        self.assertEqual(Decimal(data["total_price"]), (self.product.price + self.variant.price_modifier) * 2)
        self.assertIn("product", data)
        self.assertIn("variant", data)

    def test_cart_item_serializer_write(self):
        # Test de désérialisation avec product_id et variant_id
        data = {
            "product_id": self.product.id,
            "variant_id": self.variant.id,
            "quantity": 3
        }
        serializer = CartItemSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        # Note: pour créer réellement un item, il faut passer l'instance du panier
        # Ici on teste juste la validation des champs write_only

    # --- CartSerializer ---
    def test_cart_serializer(self):
        serializer = CartSerializer(self.cart)
        data = serializer.data
        self.assertEqual(data["total_items"], 2)
        self.assertEqual(Decimal(data["subtotal"]), self.cart_item.total_price)
        self.assertEqual(Decimal(data["total_price"]), self.cart_item.total_price)
        self.assertEqual(len(data["items"]), 1)

    # --- AddToCartSerializer ---
    def test_add_to_cart_serializer_valid(self):
        data = {
            "product_id": self.product.id,
            "variant_id": self.variant.id,
            "quantity": 2
        }
        serializer = AddToCartSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_add_to_cart_serializer_invalid_product(self):
        data = {"product_id": 99999, "quantity": 1}
        serializer = AddToCartSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("product_id", serializer.errors)

    def test_add_to_cart_serializer_invalid_variant(self):
        data = {
            "product_id": self.product.id,
            "variant_id": 99999,
            "quantity": 1
        }
        serializer = AddToCartSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("variant_id", serializer.errors)

    # --- UpdateCartItemSerializer ---
    def test_update_cart_item_serializer_valid(self):
        data = {"quantity": 5}
        serializer = UpdateCartItemSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["quantity"], 5)

    def test_update_cart_item_serializer_invalid_quantity(self):
        data = {"quantity": 0}
        serializer = UpdateCartItemSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("quantity", serializer.errors)

    # --- OrderItemSerializer ---
    def test_order_item_serializer(self):
        order = Order.objects.create(
            order_number="ORD-TEST",
            customer=self.customer,
            subtotal=Decimal("100"),
            total_price=Decimal("100")
        )
        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            product_name=self.product.name,
            product_sku=self.product.sku,
            unit_price=self.product.price,
            quantity=1,
            total_price=self.product.price
        )
        serializer = OrderItemSerializer(order_item)
        data = serializer.data
        self.assertEqual(data["quantity"], 1)
        self.assertEqual(Decimal(data["unit_price"]), self.product.price)

    # --- OrderSerializer ---
    def test_order_serializer(self):
        order = Order.objects.create(
            order_number="ORD-SER",
            customer=self.customer,
            subtotal=Decimal("500"),
            total_price=Decimal("500"),
            status="pending"
        )
        OrderItem.objects.create(
            order=order,
            product=self.product,
            product_name=self.product.name,
            product_sku=self.product.sku,
            unit_price=self.product.price,
            quantity=1,
            total_price=self.product.price
        )
        serializer = OrderSerializer(order)
        data = serializer.data
        self.assertEqual(data["order_number"], "ORD-SER")
        self.assertEqual(data["status"], "pending")
        self.assertEqual(len(data["items"]), 1)

    # --- CheckoutSerializer ---
    def test_checkout_serializer_valid(self):
        data = {
            "cart_id": str(self.cart.id),
            "email": "buyer@example.com",
            "agree_terms": True,
            "payment_method": "credit_card"
        }
        serializer = CheckoutSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_checkout_serializer_agree_terms_required(self):
        data = {
            "cart_id": str(self.cart.id),
            "email": "buyer@example.com",
            "agree_terms": False
        }
        serializer = CheckoutSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("agree_terms", serializer.errors)

    def test_checkout_serializer_invalid_cart_id(self):
        data = {
            "cart_id": "00000000-0000-0000-0000-000000000000",
            "email": "buyer@example.com",
            "agree_terms": True
        }
        serializer = CheckoutSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("cart_id", serializer.errors)

    def test_checkout_serializer_field_defaults(self):
        data = {
            "cart_id": str(self.cart.id),
            "email": "buyer@example.com",
            "agree_terms": True
        }
        serializer = CheckoutSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        validated = serializer.validated_data
        self.assertEqual(validated.get("payment_method"), "A la livraison")  # default
        self.assertEqual(validated.get("subscribe_newsletter"), False)