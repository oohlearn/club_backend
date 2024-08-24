from rest_framework import serializers
from .models import Product, Photo


# 商品
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['image_data', 'description']


class ProductSerializer(serializers.ModelSerializer):
    image_index = serializers.ImageField(max_length=None, use_url=True)
    photos = PhotoSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ["id", "title", "price", "discount_price", "state_tag",
                  "description", "on_sell", "on_discount", "image_index",
                  "photos"]


# # 購物車
# class CartProductsSerializer(serializers.ModelSerializer):
#     title = serializers.CharField(max_length=500)
#     price = serializers.IntegerField()
#     image = serializers.ImageField(max_length=None, use_url=True)
#     qty = serializers.IntegerField()


# class CartSerializer(serializers.ModelSerializer):
#     products = CartProductsSerializer(many=True)

#     class Meta:
#         model = ProductCart
#         fields = ["id", "title", "price", "qty", "total", "image", "need_deliver_paid"]

# # 購買人資訊
# # class OrderSerializer(serializers.ModelSerializer):
