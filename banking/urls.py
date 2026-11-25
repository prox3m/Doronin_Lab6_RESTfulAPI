from rest_framework.routers import DefaultRouter
from .views import CreditViewSet, DepositViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'credits', CreditViewSet, basename='credit')
router.register(r'deposit', DepositViewSet, basename='deposit')
router.register(r'transaction', TransactionViewSet, basename='transaction')

urlpatterns = router.urls