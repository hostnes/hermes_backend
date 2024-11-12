from django.shortcuts import get_object_or_404
from rest_framework import generics, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Category, SubCategory, Product, Region, District, Conversation, Message, ProductImage, \
    Favorites
from .serializers import (
    UserSerializer, CategorySerializer, SubCategorySerializer, ProductSerializer,
    RegionSerializer, DistrictSerializer, ConversationSerializer, MessageSerializer, ProductImageSerializer,
    ConversationDetailSerializer, FavoritesSerializer
)
from django_filters import rest_framework as filters


class UserFilter(filters.FilterSet):
    email = filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = User
        fields = ['email', 'password']


# Для пользователей
class UserListCreateView(generics.ListCreateAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Для категорий и подкатегорий
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryListCreateView(generics.ListCreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


# Для продуктов

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()

        # Получение параметров запроса
        title = self.request.query_params.get('title', None)
        condition = self.request.query_params.get('condition', None)
        sub_category = self.request.query_params.get('sub_category', None)
        price_min = self.request.query_params.get('price_min', None)
        price_max = self.request.query_params.get('price_max', None)
        region = self.request.query_params.get('region', None)
        district = self.request.query_params.get('district', None)
        owner_id = self.request.query_params.get('owner_id', None)
        sort_by = self.request.query_params.get('sort_by', None)
        is_active = self.request.query_params.get('is_active', None)

        print(is_active)

        if is_active == "true":
            queryset = queryset.filter(is_active=True)
        elif is_active == "false":
            queryset = queryset.filter(is_active=False)

        if title:
            queryset = queryset.filter(title__icontains=title)

        # Фильтрация по состоянию товара (если не пустое)
        if condition:
            queryset = queryset.filter(condition=condition)

        # Фильтрация по подкатегории (если не пустое)
        if sub_category:
            queryset = queryset.filter(sub_category=sub_category)

        # Фильтрация по минимальной цене (если передана)
        if price_min:
            queryset = queryset.filter(cost__gte=price_min)

        # Фильтрация по максимальной цене (если передана)
        if price_max:
            queryset = queryset.filter(cost__lte=price_max)

        # Фильтрация по региону владельца (если не пустое)
        if region:
            queryset = queryset.filter(owner__district__region=region)

        # Фильтрация по району владельца (если не пустое)
        if district:
            queryset = queryset.filter(owner__district=district)

        # Фильтрация по владельцу (если не пустое)
        if owner_id:
            queryset = queryset.filter(owner__id=owner_id)

        # Сортировка по дате или цене (если указаны корректные параметры)
        if sort_by:
            queryset = queryset.order_by(sort_by)

        return queryset




class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Для регионов и районов
class RegionListCreateView(generics.ListCreateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class DistrictListCreateView(generics.ListCreateAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


# Для бесед
class ConversationListCreateView(generics.ListCreateAPIView):
    serializer_class = ConversationSerializer

    def get_queryset(self):
        queryset = Conversation.objects.all().order_by('-updated_at')  # Sort by updated_at in descending order
        user_ids = self.request.query_params.getlist('user_id')

        if user_ids:
            for user_id in user_ids:
                queryset = queryset.filter(participants__id=user_id)

        return queryset.distinct()


class ConversationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationDetailSerializer


class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ProductImageListCreateView(generics.ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def perform_create(self, serializer):
        product_id = self.request.data.get('product')
        product = Product.objects.get(id=product_id)

        # Проверяем, сколько изображений уже загружено для продукта
        if product.images.count() >= 8:
            raise serializers.ValidationError("Нельзя загрузить больше 8 изображений для одного продукта.")

        serializer.save(product=product)

class ProductImageUploadView(APIView):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        images = request.FILES.getlist('images')

        for image in images:
            ProductImage.objects.create(product=product, image=image)

        return Response({"success": True, "message": "Images uploaded successfully."})


class FavoritesListCreateView(generics.ListCreateAPIView):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer


class FavoritesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
