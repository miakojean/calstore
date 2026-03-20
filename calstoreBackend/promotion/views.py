from django.shortcuts import render
from django.utils import timezone
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (PromotionSerializer, FlashSaleSerializer, FlashSaleSimpleSerializer)
from .models import Promotion, FlashSale

# --- VUE 1 : La Promotion "Principale" (La plus récente et active) ---
class MainPromotionView(APIView):
    """
    Récupère une seule promotion : la plus récente et active.
    Idéal pour une bannière d'accueil.
    """
    def get(self, request):
        now = timezone.now()

        # On cherche la dernière promotion active
        # Critères : active, status 'active', date début passée, date fin future (ou nulle)
        main_promo = Promotion.objects.filter(
            is_active=True,
            status='active',
            start_date__lte=now
        ).filter(
            Q(end_date__gte=now) | Q(end_date__isnull=True)
        ).order_by('-created_at').first() # .first() renvoie l'objet ou None

        if main_promo:
            serializer = PromotionSerializer(main_promo, context={'request': request})
            return Response({
                'status': 'success',
                'message': 'Promotion principale récupérée',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'info',
                'message': 'Aucune promotion principale active pour le moment',
                'data': None
            }, status=status.HTTP_200_OK) # 200 car ce n'est pas une erreur technique, juste un vide


# --- VUE 2 : Liste des Promotions en cours ---
class ActivePromotionsView(APIView):
    """
    Liste toutes les promotions valides actuellement.
    """
    def get(self, request):
        now = timezone.now()

        # Même logique de filtrage, mais on récupère tout (.all())
        active_promotions = Promotion.objects.filter(
            is_active=True,
            status='active',
            start_date__lte=now
        ).filter(
            Q(end_date__gte=now) | Q(end_date__isnull=True)
        ).order_by('-created_at')

        serializer = PromotionSerializer(active_promotions, many=True, context={'request': request})

        return Response({
            'status': 'success',
            'message': f'{active_promotions.count()} promotions actives trouvées',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


# --- VUE 3 (Bonus) : Les Ventes Flash en cours ---
class ActiveFlashSalesView(APIView):
    """
    Liste les ventes flash en cours (différent des promotions classiques)
    """
    def get(self, request):
        now = timezone.now()
        
        # Filtrer les ventes flash actives dans le temps
        flash_sales = FlashSale.objects.filter(
            is_active=True,
            start_time__lte=now,
            end_time__gte=now
        )
        
        serializer = FlashSaleSerializer(flash_sales, many=True, context={'request': request})
        
        return Response({
            'status': 'success',
            'message': 'Ventes flash en cours récupérées',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class CurrentFlashSaleView(APIView):
    """
    Retourne la vente flash en cours avec ses produits (structure plate).
    """
    def get(self, request):
        now = timezone.now()

        flash_sale = FlashSale.objects.filter(
            is_active=True,
            start_time__lte=now,
            end_time__gte=now
        ).prefetch_related('flashsaleproduct_set__product').first()

        if not flash_sale:
            return Response({
                'status': 'info',
                'message': 'Aucune vente flash en cours',
                'data': None
            }, status=status.HTTP_200_OK)

        serializer = FlashSaleSimpleSerializer(flash_sale, context={'request': request})

        return Response({
            'status': 'success',
            'message': 'Vente flash en cours récupérée',
            'data': serializer.data
        }, status=status.HTTP_200_OK)