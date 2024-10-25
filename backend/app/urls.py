from django.urls import path
from .views import (
    UserListCreateView, UserDetailView, CategoryListCreateView, SubCategoryListCreateView,
    ProductListCreateView, ProductDetailView, RegionListCreateView, DistrictListCreateView,
    ConversationListCreateView, ConversationDetailView, MessageListCreateView, MessageDetailView,
    ProductImageListCreateView, ProductImageUploadView, FavoritesListCreateView, FavoritesDetailView
)

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('subcategories/', SubCategoryListCreateView.as_view(), name='subcategory-list-create'),

    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    path('regions/', RegionListCreateView.as_view(), name='region-list-create'),
    path('districts/', DistrictListCreateView.as_view(), name='district-list-create'),

    path('conversations/', ConversationListCreateView.as_view(), name='conversation-list-create'),
    path('conversations/<int:pk>/', ConversationDetailView.as_view(), name='conversation-detail'),

    path('messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),

    path('product-images/', ProductImageListCreateView.as_view(), name='product-image-list-create'),
    path('products/<int:product_id>/upload-images/', ProductImageUploadView.as_view(), name='upload_product_images'),

    path('favorites/', FavoritesListCreateView.as_view(), name='favorites-image-list-create'),
    path('favorites/<int:favorit_id>/', FavoritesDetailView.as_view(), name='favorites-detail'),
]
