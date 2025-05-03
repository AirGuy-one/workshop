from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
)

from .models import Part, PartCategory, Order, OrderItem, OrderStatus
from .serializers import CreateOrderSerializer, AddItemSerializer

User = get_user_model()
ADMIN_USER = User.objects.get(username='admin')


@api_view(['GET'])
def get_parts(request):
    parts = Part.objects.all()
    items = []
    for part in parts:
        items.append({
            'id': part.id,
            'name': part.name,
            'category_name': part.category.name,
            'voltage': part.voltage,
            'power': part.power,
            'datasheet_url': part.datasheet_file.url if part.datasheet_file else None,
            'schematic_url': part.schematic.url if part.schematic else None,
            'created_at': part.created_at.isoformat()
        })
    return Response({'items': items}, status=HTTP_200_OK)


@api_view(['GET'])
def get_part_detail(request, part_id):
    part = get_object_or_404(Part, id=part_id)
    data = {
        'name': part.name,
        'category_name': part.category.name,
        'voltage': part.voltage,
        'power': part.power,
        'datasheet_url': part.datasheet_file.url if part.datasheet_file else None,
        'schematic_url': part.schematic.url if part.schematic else None,
        'created_at': part.created_at.isoformat()
    }
    return Response(data, status=HTTP_200_OK)


@api_view(['GET'])
def get_categories(request):
    categories = PartCategory.objects.all()
    result = [{'id': c.id, 'name': c.name} for c in categories]
    return Response(result, status=HTTP_200_OK)


@extend_schema(request=CreateOrderSerializer, responses={201: dict})
@api_view(['POST'])
def create_order(request):
    serializer = CreateOrderSerializer(data=request.data)
    if serializer.is_valid():
        part_id = serializer.validated_data['part_id']
        order = Order.objects.create(user=ADMIN_USER)
        OrderItem.objects.create(order=order, part_id=part_id, quantity=1)
        return Response({'id': order.id}, status=HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_order_positions_quantity(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=ADMIN_USER)
    quantity = sum(item.quantity for item in order.items.all())
    return Response({'positions_quantity': quantity}, status=HTTP_200_OK)


@api_view(['GET'])
def get_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=ADMIN_USER)
    items = [{'part_id': item.part_id, 'quantity': item.quantity} for item in order.items.all()]
    return Response({
        'created_at': order.created_at.isoformat(),
        'status': order.status,
        'items': items
    }, status=HTTP_200_OK)


@extend_schema(request=AddItemSerializer, responses={201: dict})
@api_view(['POST'])
def add_item_to_order(request, order_id):
    serializer = AddItemSerializer(data=request.data)
    if serializer.is_valid():
        part_id = serializer.validated_data['part_id']
        order = get_object_or_404(Order, id=order_id, user=ADMIN_USER)

        item, created = OrderItem.objects.get_or_create(
            order=order, part_id=part_id, defaults={'quantity': 1}
        )
        if not created:
            item.quantity += 1
            item.save()

        return Response({'message': 'Item added'}, status=HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def complete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=ADMIN_USER)
    order.status = OrderStatus.COMPLETED
    order.save()
    return Response(status=HTTP_204_NO_CONTENT)
