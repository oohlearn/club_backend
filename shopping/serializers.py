from rest_framework import serializers
from .models import Product, Photo, Size, ProductCode, Order, Cart, CartItem
from activity.serializers import TicketDiscountCodeSerializer, SeatFroNumberRowSerializer, SeatSerializer
from user.serializers import CustomerSerializer


# 商品
class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['size', "group", 'description']


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['image_data', 'description', "level"]


class ProductSerializer(serializers.ModelSerializer):
    index_image = serializers.ImageField(max_length=None, use_url=True)
    photos = PhotoSerializer(many=True, required=False)
    size_list = SizeSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ["id", "name", "price", "discount_price", "category",
                  "quantity", "sold_qty", "description", "on_sell", 
                  "on_discount", "state_tag",
                  "index_image", "photos", "size_list"]


# 商品優惠碼
class ProductDiscountCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCode
        fields = ["name", "code", "discount", "is_valid", "end_date", "description"]


# 購物車
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(required=False)
    seat = SeatSerializer(required=False)
    seat_v2 = SeatFroNumberRowSerializer(required=False)

    class Meta:
        model = CartItem
        fields = ["product", "size", "quantity",
                  "seat", "seat_v2"]


class CartSerializer(serializers.ModelSerializer):
    cartItem = CartItemSerializer(many=True)
    ticket_discount_code = TicketDiscountCodeSerializer(required=False)
    product_code = ProductDiscountCodeSerializer(required=False)

    class Meta:
        model = Cart
        fields = ["created_at", "cartItem", "ticket_discount_code",
                  "product_code", "total_price", "need_deliver_paid", "status",
                  "shipping_fee"]

    def create(self, validated_data):
        cart_items_data = validated_data.pop('cartItem')
        cart = Cart.objects.create(**validated_data)
        for item_data in cart_items_data:
            CartItem.objects.create(cart=cart, **item_data)
        return cart


# 訂單
class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)
    customer = CustomerSerializer()

    def update(self, instance, validated_data):
        customer_data = validated_data.pop('customer')
        customer_serializer = CustomerSerializer(instance.customer, data=customer_data)
        if customer_serializer.is_valid():
            customer_serializer.save()
        return super().update(instance, validated_data)

    class Meta:
        model = Order
        fields = ["id", "created_at", "customer", "cart",
                  "total_price", "status"]
