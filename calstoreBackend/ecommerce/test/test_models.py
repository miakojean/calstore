from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from ecommerce.models import Category, Product, ProductImage, Order, Coupon, Address, GuestCustomer

class ModelLogicTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Bio", slug="bio")
        self.product = Product.objects.create(
            name="Mangue José",
            slug="mangue-jose",
            category=self.category,
            price=10.00,
            compare_price=15.00,
            quantity=10
        )

    def test_product_properties(self):
        """Vérifie les calculs de promotion et de stock"""
        # Test remise
        self.assertTrue(self.product.is_on_sale)
        self.assertEqual(self.product.discount_percentage, 33)
        
        # Test stock
        self.assertTrue(self.product.in_stock)
        self.product.quantity = 0
        self.product.save()
        self.assertFalse(self.product.in_stock)

    def test_order_number_generation(self):
        """Vérifie qu'un numéro de commande est généré à la création"""
        order = Order.objects.create(
            subtotal=100,
            total_price=100,
            guest_email="test@example.com"
        )
        self.assertTrue(order.order_number.startswith("ORD-"))
        self.assertEqual(len(order.order_number), 14)

    def test_address_validation(self):
        """Vérifie qu'une adresse doit être liée à un client ou un invité"""
        address = Address(
            address_line_1="Rue des Jardins",
            city="Abidjan",
            address_type='shipping'
        )
        with self.assertRaises(ValidationError):
            address.clean()

    def test_coupon_validity(self):
        """Vérifie la logique de validité des coupons"""
        coupon = Coupon.objects.create(
            code="PROMO2026",
            discount_type='percentage',
            discount_value=10,
            valid_from=timezone.now() - timedelta(days=1),
            valid_until=timezone.now() + timedelta(days=1),
            is_active=True
        )
        self.assertTrue(coupon.is_valid)
        
        # Expiration
        coupon.valid_until = timezone.now() - timedelta(hours=1)
        coupon.save()
        self.assertFalse(coupon.is_valid)