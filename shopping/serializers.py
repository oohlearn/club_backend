from rest_framework import serializers
from .models import Product, Photo, Size, ProductCode, Order, OrderItem, Customer
from activity.serializers import TicketDiscountCodeSerializer, SeatFroNumberRowSerializer, SeatSerializer


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


# 購買者
class CustomerSerialize(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


# 訂單
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(required=False)
    ticket_discount_code = TicketDiscountCodeSerializer(required=False)
    product_code = ProductDiscountCodeSerializer(required=False)
    seat = SeatSerializer(required=False)
    seat_v2 = SeatFroNumberRowSerializer(required=False)

    class Meta:
        model = OrderItem
        fields = ["product", "size", "quantity", "ticket_discount_code", "seat",
                  "seat", "seat_v2", "product_code", "subtotal"]


class OrderSerializer(serializers.ModelSerializer):
    orderItem = OrderItemSerializer(many=True)
    customer = CustomerSerialize()

    class Meta:
        model = Order
        fields = ["id", "created_at", "customer", "orderItem",
                  "need_deliver_paid", "total_price", "status"]
