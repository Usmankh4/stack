from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from store.views import (
    NewArrivalsAPIView, 
    BestSellersAPIView,
    PhoneVariantDetailAPIView,
    AccessoryDetailAPIView
)

urlpatterns = [
    path('', RedirectView.as_view(url='/api/homepage/', permanent=False), name='index'),
    path('admin/', admin.site.urls),
    
    # API endpoints from promotions app
    path('api/', include('promotions.urls')),
    
    # API endpoints from store app
    path('api/new-arrivals/', NewArrivalsAPIView.as_view(), name='new_arrivals'),
    path('api/best-sellers/', BestSellersAPIView.as_view(), name='best_sellers'),
    path('api/phones/<slug:slug>/', PhoneVariantDetailAPIView.as_view(), name='phone_detail'),
    path('api/accessories/<slug:slug>/', AccessoryDetailAPIView.as_view(), name='accessory_detail'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
