from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='pokemons', blank=True, null=True)
    
    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, null=True, on_delete=models.SET_NULL)
    latitude = models.FloatField('Lat')
    longitude = models.FloatField('Lon')
