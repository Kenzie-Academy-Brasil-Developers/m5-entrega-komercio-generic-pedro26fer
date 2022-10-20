from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.ListCreateProductsView.as_view()),
    path("products/<pk>/", views.RetrieveTotalAndPartialUpdateView.as_view())
]
