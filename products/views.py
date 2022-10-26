from .models import Product
from rest_framework import generics
from .serializers import ProductDetailSerializer, ProductGeneralSerializer
from .mixins import SerializerByMethodMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAutorizedToPostPatch
from rest_framework.authentication import TokenAuthentication
from products.utils import CustomRetrieveUpdateAPIView



class ListCreateProductsView(SerializerByMethodMixin, generics.ListCreateAPIView):

    
    queryset = Product
    serializer_class = ProductDetailSerializer


    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAutorizedToPostPatch]

    queryset = Product.objects.all()

    serializer_map = {
        "GET": ProductGeneralSerializer,
        "POST": ProductDetailSerializer
    }

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class RetrieveTotalAndPartialUpdateView(CustomRetrieveUpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAutorizedToPostPatch]

    queryset = Product.objects.all()

    serializer_class = ProductDetailSerializer
