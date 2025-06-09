from django.urls import path
from .views import FlashDealsAPIView, HomepageAPIView

urlpatterns = [
    path('flash-deals/', FlashDealsAPIView.as_view(), name='flash-deals'),
    path('homepage/', HomepageAPIView.as_view(), name='homepage'),
]
