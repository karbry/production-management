from django.urls import path, include
from django.contrib.auth.decorators import login_required
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'orders', views.OrderViewSet)
# router.register(r'products', views.ProductViewSet)
# router.register(r'customers', views.CustomerViewSet)

urlpatterns = [
    path('', login_required(views.OrdersForLocalizationListView.as_view()), name='orders_for_localization'),
    path('all', login_required(views.AllOrdersListView.as_view()), name='all_orders'),
    path('<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('api/', include(router.urls)),
]