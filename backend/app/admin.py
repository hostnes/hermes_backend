from django.contrib import admin
from .models import User, Category, SubCategory, Product, Region, District, Conversation, Message, ProductImage


# Регистрация модели User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'gender', 'phone_number']  # Поля, отображаемые в списке
    search_fields = ['email', 'name', 'phone_number']  # Поля, по которым можно искать
    list_filter = ['gender']  # Фильтры по полям


# Регистрация модели Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'condition']
    search_fields = ['title', 'owner__email']
    list_filter = ['condition']


# Регистрация модели Conversation
@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['created_at']
    search_fields = ['participants__email']
    filter_horizontal = ['participants']  # Добавляет удобный выбор участников в админке


# Регистрация модели Message
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'sender', 'text', 'sent_at']
    search_fields = ['sender__email', 'text']
    list_filter = ['sent_at']

@admin.register(ProductImage)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ['product', 'image']
    search_fields = ['product']

#
# # Регистрация модели Region
# @admin.register(Region)
# class RegionAdmin(admin.ModelAdmin):
#     list_display = ['title']
#     search_fields = ['title']
#
#
# # Регистрация модели District
# @admin.register(District)
# class DistrictAdmin(admin.ModelAdmin):
#     list_display = ['title', 'region']
#     search_fields = ['title']
#     list_filter = ['region']
#
# # Регистрация модели Category
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['title']
#     search_fields = ['title']
#
#
# # Регистрация модели SubCategory
# @admin.register(SubCategory)
# class SubCategoryAdmin(admin.ModelAdmin):
#     list_display = ['title', 'category']
#     search_fields = ['title']
#     list_filter = ['category']