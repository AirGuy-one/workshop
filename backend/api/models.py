from django.contrib.auth import get_user_model

from django.db import models

User = get_user_model()


class OrderStatus(models.TextChoices):
    CREATED = 'CREATED'
    PAID = 'PAID'
    SHIPPED = 'SHIPPED'
    CANCELLED = 'CANCELLED'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.CREATED
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class PartCategory:
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Part(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(PartCategory, on_delete=models.CASCADE)

    voltage = models.FloatField()
    power = models.FloatField()

    datasheet_file = models.FileField(upload_to='datasheets/', blank=True, null=True)
    schematic = models.FileField(upload_to='schematics/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    compatible_with = models.ManyToManyField(
        'self',
        symmetrical=True,
        blank=True,
        through='PartCompatibility',
        related_name='compatible_parts'
    )

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.part.name}"


class PartCompatibility(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='compatibility_links')
    compatible_with = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='reverse_compatibility_links')

    class Meta:
        unique_together = ('part', 'compatible_with')
