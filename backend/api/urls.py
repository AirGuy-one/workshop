from django.urls import path

from .views import (
    get_parts,
    get_categories,
    create_order,
    get_order_positions_quantity,
    get_order_detail,
    add_item_to_order,
    complete_order,
    get_order_history,
)

urlpatterns = [
    path('parts/', get_parts, name='part-list'),
    path('categories/', get_categories, name='category-list'),
    path('orders/', create_order, name='order-create'),
    path('orders/<int:order_id>/', get_order_detail, name='order-detail'),
    path('orders/<int:order_id>/positions-quantity/', get_order_positions_quantity, name='order-positions-quantity'),
    path('orders/<int:order_id>/add-item/', add_item_to_order, name='order-add-item'),
    path('orders/<int:order_id>/complete/', complete_order, name='order-complete'),
    path('orders/history/', get_order_history, name='order-history'),
]
