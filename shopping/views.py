from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound


from .serializers import (ProductSerializer, OrderSerializer,
                          ProductDiscountCodeSerializer, CartSerializer,
                          SizeSerializer)
from .models import Product, Order, ProductCode, Cart, CartItem, Customer, Size
from django.db import transaction


# 商品
# 分頁
class ProductListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class SizeViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = SizeSerializer

    def get_queryset(self):
        product_pk = self.kwargs.get('product_pk')
        if product_pk:
            product = Product.objects.filter(pk=product_pk).first()
            if not product:
                raise NotFound('Product not found')
            return Size.objects.filter(product=product)
        return Size.objects.all()

    def perform_create(self, serializer):
        product_pk = self.kwargs.get('product_pk')
        product = Product.objects.filter(pk=product_pk).first()
        if not product:
            raise NotFound('Product not found')
        serializer.save(product=product)

    @action(detail=True, methods=['post'])
    def update_pre_sold(self, request, id, pk=None):
        try:
            product = get_object_or_404(Product, id=id)
            size = get_object_or_404(Size, pk=pk, product=product)
            quantity = int(request.data.get('quantity', 0))

            with transaction.atomic():
                size = Size.objects.select_for_update().get(pk=pk)
                if size.available_quantity() >= quantity:
                    size.pre_sold_qty += quantity
                    size.save()
                    return Response({'status': 'success'}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'error', 'message': '庫存不足'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def release_pre_sold(self, request, id, pk=None):
        size = self.get_object()
        quantity = int(request.data.get('quantity', 0))

        with transaction.atomic():
            size = Size.objects.select_for_update().get(pk=pk)
            size.pre_sold_qty = max(0, size.pre_sold_qty - quantity)
            size.save()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination = ProductListPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        data = serializer.data
        formatted_data = [{"name": item["name"], **item} for item in data]

        return Response({
            "products": formatted_data
        }, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = Product.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = Product.objects.filter(id=id)
        return queryset


# 購物車
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        data = serializer.data
        formatted_data = [{"created_at": item["created_at"], **item} for item in data]

        return Response({
            "cart": formatted_data
        }, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = Cart.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = Cart.objects.filter(id=id)
        return queryset

    @transaction.atomic
    def create(self, request):
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))
        size_id = request.data.get("size")

        size = Size.objects.select_for_update().get(id=size_id)

        if size.available_quantity() >= quantity:
            size.pre_sold_qty += quantity
            size.save()

            cart, created = Cart.objects.get_or_create(customer=request.user.customer)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product_id=product_id,
                size_id=size_id,
                defaults={'quantity': 0}
            )
            cart_item.quantity += quantity
            cart_item.save()

            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'error', 'message': '庫存不足'}, status=status.HTTP_400_BAD_REQUEST)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        data = serializer.data
        formatted_data = [{"id": item["id"], **item} for item in data]

        return Response({
            "order": formatted_data
        }, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = Order.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = Order.objects.filter(id=id)
        return queryset


class ProductCodeViewSet(viewsets.ModelViewSet):
    queryset = ProductCode.objects.all()
    serializer_class = ProductDiscountCodeSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        data = serializer.data
        formatted_data = [{"name": item["name"], **item} for item in data]

        return Response({
            "productCode": formatted_data
        }, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = ProductCode.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = ProductCode.objects.filter(id=id)
        return queryset


class CreateCartView(APIView):
    @transaction.atomic
    def post(self, request):
        cart_items_data = request.data.get('cartItems', [])
        ticket_items_data = request.data.get('ticketItems', [])

        try:
            # 创建一个没有客户信息的购物车
            cart = Cart.objects.create()

            for item_data in cart_items_data:
                CartItem.objects.create(
                    cart=cart,
                    product_id=item_data['product'],
                    size=item_data.get('size'),
                    quantity=item_data['quantity']
                )

            for item_data in ticket_items_data:
                CartItem.objects.create(
                    cart=cart,
                    seat_id=item_data.get('seat'),
                    seat_v2_id=item_data.get('seat_v2')
                )

            cart.update_total_price()

            return Response({
                'success': True,
                'cart_id': cart.id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class CartDetailView(RetrieveUpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'success': True,
            'cart': serializer.data,
        })


class CreateOrderView(RetrieveUpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # 创建或更新客户信息
        customer_data = request.data.get('customer', {})
        customer, created = Customer.objects.get_or_create(
            email=customer_data.get('email'),
            defaults=customer_data
        )

        # 更新购物车的客户信息
        instance.customer = customer
        instance.save()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # 创建订单
        order = Order.objects.create(
            cart=instance,
            status='pending',
            total_amount=instance.total_price
        )
        order_serializer = OrderSerializer(order)

        return Response({
            'success': True,
            'cart': serializer.data,
            'order': order_serializer.data
        })
