from rest_framework.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from authapp import views

urlpatterns = [
    path('api/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]