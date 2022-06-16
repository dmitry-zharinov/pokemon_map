from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True, null=True)
    title_jp = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='pokemons', blank=True, null=True)
    previous_evolution = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, null=True, on_delete=models.SET_NULL)
    latitude = models.FloatField('Lat')
    longitude = models.FloatField('Lon')
    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()

    level = models.IntegerField('Level')
    health = models.IntegerField('Health')
    strength = models.IntegerField('Strength')
    defence = models.IntegerField('Defence')
    stamina = models.IntegerField('Stamina')

