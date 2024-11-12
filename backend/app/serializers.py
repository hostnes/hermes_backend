from rest_framework import serializers
from .models import User, Category, SubCategory, Product, Region, District, Conversation, Message, CONDITION, \
    ProductImage




class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'title']


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'sub_categories']

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'title']

# class DistrictSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = District
#         fields = ['id', 'title']


class RegionSerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(many=True, read_only=True)

    class Meta:
        model = Region
        fields = ['id', 'title', 'districts']


class RegionUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'title']


class DistrictUserSerializer(serializers.ModelSerializer):
    region = serializers.CharField(source='region.title', read_only=True)

    class Meta:
        model = District
        fields = ['id', 'title', 'region']


class CategoryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

class SubCategoryUserSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title')

    class Meta:
        model = SubCategory
        fields = ['id', 'title', 'category']



class UserSerializer(serializers.ModelSerializer):
    district_details = serializers.SerializerMethodField()  # Поле не обязательно

    class Meta:
        model = User
        fields = ['id', 'photo', 'email', 'name', 'description', 'gender', 'phone_number', "password", 'district', 'district_details', 'district']

    def get_district_details(self, obj):
        # Проверяем, есть ли связанный объект district
        if obj.district:
            # Сериализуем объект district с помощью DistrictUserSerializer
            return DistrictUserSerializer(obj.district).data
        return None  # Если district нет, возвращаем None

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Use PrimaryKeyRelatedField for sender
    sender_detail = UserSerializer(source='sender', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'text', 'sent_at', 'sender_detail']


class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'user', 'product']


class ConversationSerializer(serializers.ModelSerializer):
    # Accept IDs as input while returning full user data on output
    participant_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        source='participants'  # This maps to the participants field on the model
    )
    participants = UserSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participant_ids', 'participants', 'last_message', 'created_at', 'updated_at']

    def get_last_message(self, obj):
        last_message = obj.messages.last()
        return MessageSerializer(last_message).data if last_message else None

    def create(self, validated_data):
        # Extract participants from validated data
        participants = validated_data.pop('participants')
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        return conversation


class ConversationDetailSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages', 'created_at', 'updated_at']



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image']

    def create(self, validated_data):
        # Вы можете добавить здесь дополнительную валидацию, если это необходимо
        return ProductImage.objects.create(**validated_data)


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)  # Write-only for creation
    owner_details = UserSerializer(source='owner', read_only=True)  # Read-only for retrieval
    condition = serializers.ChoiceField(choices=CONDITION)
    images = ProductImageSerializer(many=True, required=False)

    # Use PrimaryKeyRelatedField for creation, and a nested serializer for read operations
    sub_category = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all(), write_only=True)
    sub_category_details = SubCategoryUserSerializer(source='sub_category', read_only=True)  # Read-only for retrieval

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'cost', 'date', 'condition', 'owner', 'owner_details', 'sub_category',
                  'sub_category_details', 'images', 'is_active']

    def create(self, validated_data):
        images_data = validated_data.pop('images', None)
        print(f"Received images data: {images_data}")  # Debugging line

        product = Product.objects.create(**validated_data)

        if images_data:
            for image_data in images_data:
                print(f"Creating image entry for product: {product.id}")  # Debugging line
                ProductImage.objects.create(product=product, **image_data)

        return product



