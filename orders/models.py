from django.conf import settings
from django.db import models
from django.shortcuts import reverse


class ItemTag(models.Model):
    """
    A model for the item tags with selectable
    Bootstrap colours.
    """
    TAG_COLOURS = (
        ('danger', 'Red'),
        ('success', 'Green'),
        ('info', 'Blue'),
        ('warning', 'Yellow'),
        ('secondary', 'Gray')
    )

    name = models.CharField(max_length=10)
    colour = models.CharField(choices=TAG_COLOURS,
                              max_length=10, default='Red')

    def __str__(self):
        return self.name


class Item(models.Model):
    """
    A model for the items/products.
    Urls are slug based.
    """
    name = models.CharField(max_length=20)
    slug = models.SlugField()
    description = models.TextField(max_length=70)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    clicks = models.IntegerField(default=0)
    tag = models.ForeignKey(
        ItemTag, null=True, blank=True, on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return reverse('orders:product', kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse('orders:add_to_cart', kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse('orders:remove_from_cart', kwargs={
            'slug': self.slug
        })

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    """
    A model for the order items
    to be collected by the order.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.item.name


class Order(models.Model):
    """
    A model to collect
    the order items in 1 order
    """
    STATUS = (
        ('requested', 'Requested'),
        ('pending', 'Pending'),
        ('finished', 'Finished')
    )

    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(
        choices=STATUS, default='requested', max_length=10)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
