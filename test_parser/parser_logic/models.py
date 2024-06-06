from django.db import models


class ParsedData(models.Model):

    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.CharField(max_length=3000)
    image_url = models.URLField(max_length=400)
    discount = models.CharField(max_length=4)
    link = models.URLField(max_length=1200)

    def __str__(self):
        return (f'Name: {self.name}, price: {self.price}, description: {self.description},'
                f' image_url: {self.image_url}, discount: {self.discount}')

    class Meta:
        verbose_name = 'OZON товар'
        verbose_name_plural = 'Товары OZON\'a'
