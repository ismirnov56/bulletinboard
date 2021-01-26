from django.db import models
from uuslug import uuslug


class Country(models.Model):
    """
    Модель для стран
    """
    name = models.CharField(max_length=50, blank=False)
    slug = models.SlugField(unique=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Если при сохранении модели slug пустой, то для генерации slug используется
        uuslug: https://github.com/un33k/django-uuslug
        Также данная библиотека позволяет генерировать уникальные slug поля
        """
        if not self.slug:
            self.slug = uuslug(self.name, instance=self, max_length=50)
        super(Country, self).save(*args, **kwargs)

    def __str__(self):
        return f'id {self.id} name {self.name}'


class Region(models.Model):
    """
    Модель для регионов
    """
    name = models.CharField(max_length=50, blank=False)
    slug = models.SlugField(unique=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Аналогично модели Country
        """
        if not self.slug:
            self.slug = uuslug(self.name, instance=self, max_length=50)
        super(Region, self).save(*args, **kwargs)

    def __str__(self):
        return f'id {self.id} name {self.name}'


class City(models.Model):
    """
    Модель для городов
    """
    name = models.CharField(max_length=50, blank=False)
    slug = models.SlugField(unique=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Аналогично модели Country
        """
        if not self.slug:
            self.slug = uuslug(self.name, instance=self, max_length=50)
        super(City, self).save(*args, **kwargs)

    def __str__(self):
        return f'id {self.id} name {self.name}'