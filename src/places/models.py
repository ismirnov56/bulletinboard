from django.db import models


class Counties(models.Model):
    """
    Модель для стран
    """
    name = models.CharField(max_length=50, blank=False)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return f'id {self.id} name {self.name}'


class Regions(models.Model):
    """
    Модель для регионов
    """
    name = models.CharField(max_length=50, blank=False)
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)
    country = models.ForeignKey(Counties, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'id {self.id} name {self.name}'


class Cities(models.Model):
    """
    Модель для городов
    """
    name = models.CharField(max_length=50, blank=False)
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)
    region = models.ForeignKey(Regions, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'id {self.id} name {self.name}'
