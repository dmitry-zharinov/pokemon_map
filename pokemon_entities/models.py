from django.db import models  # noqa F401

class Pokemon(models.Model):
    """Покемон"""
    title = models.CharField(verbose_name='Наименование', max_length=200)
    title_en = models.CharField(verbose_name='Наименование на английском', max_length=200, blank=True, null=True)
    title_jp = models.CharField(verbose_name='Наименование на японском', max_length=200, blank=True, null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    image = models.ImageField(verbose_name='Изображение', upload_to='pokemons', blank=True, null=True)
    previous_evolution = models.ForeignKey('self', related_name='next_evolutions', verbose_name='Предыдущая эволюция', null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    """Сущность Покемона"""
    pokemon = models.ForeignKey(Pokemon, verbose_name='Покемон', null=True, on_delete=models.SET_NULL)
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Когда появился', null=True, blank=True)
    disappeared_at = models.DateTimeField(verbose_name='Когда исчезнет', null=True, blank=True)

    level = models.IntegerField(verbose_name='Уровень', null=True, blank=True)
    health = models.IntegerField(verbose_name='Здоровье', null=True, blank=True)
    strength = models.IntegerField(verbose_name='Сила', null=True, blank=True)
    defence = models.IntegerField(verbose_name='Защита', null=True, blank=True)
    stamina = models.IntegerField(verbose_name='Выносливость', null=True, blank=True)

