from rest_framework import serializers


class CreateOrderSerializer(serializers.Serializer):
    part_id = serializers.IntegerField()


class AddItemSerializer(serializers.Serializer):
    part_id = serializers.IntegerField()
