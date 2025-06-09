from django.utils import timezone
from ..models import FlashDeal

class FlashDealService:
    @staticmethod
    def get_active_flash_deals(limit=None):
        """
        Get all active flash deals that are currently running
        """
        now = timezone.now()
        query = FlashDeal.objects.filter(
            is_active=True,
            start_date__lte=now,
            end_date__gt=now
        )
        
        if limit:
            return query[:limit]
        return query
    
    @staticmethod
    def get_flash_deal_by_slug(slug):
        """
        Get a specific flash deal by its slug
        """
        try:
            return FlashDeal.objects.get(slug=slug, is_active=True)
        except FlashDeal.DoesNotExist:
            return None
    
    @staticmethod
    def get_upcoming_flash_deals(limit=None):
        """
        Get flash deals that haven't started yet
        """
        now = timezone.now()
        query = FlashDeal.objects.filter(
            is_active=True,
            start_date__gt=now
        ).order_by('start_date')
        
        if limit:
            return query[:limit]
        return query
