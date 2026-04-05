from django.test import TestCase, RequestFactory
from ecommerce.models import Category, Product, Cart
from ecommerce.serializers import ProductSerializer, AddToCartSerializer, CheckoutSerializer

class SerializerTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.category = Category.objects.create(name="Légumes", slug="legumes")
        self.product = Product.objects.create(
            name="Carotte",
            slug="carotte",
            category=self.category,
            price=2.50,
            is_active=True
        )
        self.cart = Cart.objects.create()

    def test_product_serializer_output(self):
        """Vérifie que les champs calculés sont présents dans le JSON"""
        request = self.factory.get('/')
        serializer = ProductSerializer(self.product, context={'request': request})
        data = serializer.data
        
        self.assertEqual(data['name'], "Carotte")
        self.assertIn('main_image_url', data)
        self.assertIn('discount_percentage', data)

    def test_add_to_cart_validation(self):
        """Vérifie la validation de l'ajout au panier"""
        # Données valides
        data = {'product_id': self.product.id, 'quantity': 2}
        serializer = AddToCartSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        # Produit inexistant
        data_invalid = {'product_id': 999, 'quantity': 1}
        serializer_invalid = AddToCartSerializer(data=data_invalid)
        self.assertFalse(serializer_invalid.is_valid())
        self.assertIn('product_id', serializer_invalid.errors)

    def test_checkout_serializer_validation(self):
        """Vérifie les contraintes du tunnel d'achat"""
        data = {
            'cart_id': self.cart.id,
            'email': 'dev@caladrius.ci',
            'agree_terms': False  # Devrait échouer
        }
        serializer = CheckoutSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('agree_terms', serializer.errors)
        
        # Correction
        data['agree_terms'] = True
        serializer = CheckoutSerializer(data=data)
        self.assertTrue(serializer.is_valid())