from django.db import models

# Create your models here.

class Storetype(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class items(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/', null=True)
    price = models.IntegerField()
    availability = models.BooleanField()
    stypetype = models.ForeignKey(Storetype, on_delete=models.CASCADE, null=True)
    def __str__(self):
        template = '{0.name} {0.description} {0.image} {0.price} {0.availability}'
        return template.format(self)

class itemsdetails(models.Model):
    color =  models.CharField(max_length=50)
    quantity = models.FloatField()
    tax = models.FloatField()
    barcode = models.CharField(max_length=200)
    county = models.CharField(max_length=50)
    items =  models.ForeignKey(items, on_delete=models.CASCADE, null=True)

class Coffee(models.Model):
    blend_name = models.CharField(max_length=100)
    roastery_name = models.CharField(max_length=100)
    date_of_roasting = models.DateField()
    price = models.IntegerField()
    description = models.CharField(max_length=1000)
    image_bag = models.ImageField(upload_to='images/', null=True)
    image_notes = models.ImageField(upload_to='images/', null=True) 
    def __str__(self):
        template = '{0.blend_name} {0.roastery_name} {0.date_of_roasting} {0.price} {0.description} {0.image_bag} {0.image_notes}'
        return template.format(self)

class cart(models.Model):
    itemsid = models.IntegerField()
