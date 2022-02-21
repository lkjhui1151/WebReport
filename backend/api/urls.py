from unicodedata import name
from django.urls import include, path
from rest_framework import routers
from . import views
from django.conf import settings
from django.conf.urls.static import static

# router = routers.DefaultRouter()
# router.register(r'company', views.CompanyViewSet)

urlpatterns = [
    path('company-list/', views.CompanyList, name="get-company"),
    path('company-detail/<int:pk>', views.CompanyDetail, name="detail-company"),
    path('company-download/<int:pk>',
         views.CompanyDownload, name="download-company"),
    path('company-add/', views.CompanyAdd, name="add-company"),
    path('company-update/<int:pk>', views.CompanyUpdate, name="update-company"),
    path('company-delete/<int:pk>', views.CompanyDelete, name="delete-company"),
]+static(settings.MEDIA_URL,
         document_root=settings.MEDIA_ROOT)
