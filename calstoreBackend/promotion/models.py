from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import User
from ecommerce.models import (
    Product, 
    Order,
    Category
)  # ou votre modèle Produit

class Promotion(models.Model):
    """
    Modèle pour les promotions avec différentes options
    """ 
    TYPE_CHOICES = [
        ('percentage', 'Pourcentage'),
        ('fixed', 'Montant fixe'),
        ('buy_one_get_one', 'Achetez un, obtenez-en un gratuit'),
        ('free_shipping', 'Livraison gratuite'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('scheduled', 'Programmée'),
        ('expired', 'Expirée'),
        ('disabled', 'Désactivée'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    # Type de promotion
    promotion_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='percentage')
    discount_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True, 
        blank=True,
        help_text="Pourcentage de réduction (0-100)"
    )
    discount_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Montant fixe de réduction"
    )
    
    # Produits concernés
    products = models.ManyToManyField(Product, related_name='promotions', blank=True)
    categories = models.ManyToManyField(Category, blank=True)  # si vous avez des catégories
    all_products = models.BooleanField(default=False, help_text="S'applique à tous les produits")
    
    # Période de validité
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    
    # Conditions
    minimum_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    minimum_quantity = models.IntegerField(null=True, blank=True)
    usage_limit = models.IntegerField(null=True, blank=True, help_text="Nombre d'utilisations maximum")
    usage_count = models.IntegerField(default=0)
    
    # Statut
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    # Code promo
    code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"
    
    def __str__(self):
        return f"{self.name} ({self.get_promotion_type_display()})"
    
    @property
    def is_valid(self):
        """Vérifie si la promotion est actuellement valide"""
        now = timezone.now()
        
        if not self.is_active or self.status != 'active':
            return False
        
        if self.start_date and self.start_date > now:
            return False
        
        if self.end_date and self.end_date < now:
            return False
        
        if self.usage_limit and self.usage_count >= self.usage_limit:
            return False
        
        return True
    
    def calculate_discount(self, original_price, quantity=1):
        """Calcule le prix après réduction"""
        if not self.is_valid:
            return original_price
        
        if self.promotion_type == 'percentage' and self.discount_percentage:
            discount = (original_price * self.discount_percentage) / 100
        elif self.promotion_type == 'fixed' and self.discount_amount:
            discount = self.discount_amount
        else:
            return original_price
        
        # Ne pas descendre en dessous de 0
        final_price = max(original_price - discount, 0)
        return final_price
    
    def applies_to_product(self, product):
        """Vérifie si la promotion s'applique à un produit spécifique"""
        if self.all_products:
            return True
        
        if self.products.filter(id=product.id).exists():
            return True
        
        # Vérifier les catégories si vous en avez
        if hasattr(product, 'category'):
            if self.categories.filter(id=product.category.id).exists():
                return True
        
        return False


class UserPromotionUsage(models.Model):
    """
    Suivi de l'utilisation des promotions par les utilisateurs
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    used_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'promotion', 'order']
        verbose_name = "Utilisation de promotion"
        verbose_name_plural = "Utilisations de promotions"


class FlashSale(models.Model):
    """
    Promotions flash limitées dans le temps
    """
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, through='FlashSaleProduct')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='flashSales/')
    
    def __str__(self):
        return self.name
    
    @property
    def is_ongoing(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time and self.is_active


class FlashSaleProduct(models.Model):
    """
    Produits spécifiques dans une vente flash avec leur propre réduction
    """
    flash_sale = models.ForeignKey(FlashSale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    flash_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_limit = models.IntegerField(null=True, blank=True)
    sold_quantity = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['flash_sale', 'product']