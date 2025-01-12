import folium
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime

from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemons = Pokemon.objects.all()
    pokemon_entities = PokemonEntity.objects.filter(
        disappeared_at__gt=localtime(),
        appeared_at__lt=localtime()
    )

    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.latitude,
            pokemon_entity.longitude,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemon_description = {
            'pokemon_id': pokemon.id,
            'title_ru': pokemon.title,
        }
        if pokemon.image:
            pokemon_description.update({'img_url': pokemon.image.url})
        pokemons_on_page.append(pokemon_description)

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        requested_pokemon = Pokemon.objects.get(id=int(pokemon_id))
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    serialized_pokemon = {
        'pokemon_id': requested_pokemon.id,
        'title_ru': requested_pokemon.title,
        'title_en': requested_pokemon.title,
        'title_jp': requested_pokemon.title,
        'description': requested_pokemon.description,
        'img_url': request.build_absolute_uri(requested_pokemon.image.url),
        'previous_evolution':
            get_previous_evolution(request, requested_pokemon),
        "next_evolution": get_next_evolution(request, requested_pokemon),
        }

    requested_entities = PokemonEntity.objects.filter(
        pokemon=requested_pokemon,
        disappeared_at__date__gte=localtime(),
        appeared_at__date__lte=localtime()
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    # for pokemon_entity in requested_pokemon['entities']:
    for pokemon_entity in requested_entities:
        add_pokemon(
            folium_map, pokemon_entity.latitude,
            pokemon_entity.longitude,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': serialized_pokemon
    })


def get_previous_evolution(request, pokemon):
    if pokemon.previous_evolution:
        return {
            'title_ru': pokemon.previous_evolution.title,
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url':
                request.build_absolute_uri(
                    pokemon.previous_evolution.image.url)
        }


def get_next_evolution(request, pokemon):
    if not pokemon.next_evolutions.all():
        return None
    pokemon = pokemon.next_evolutions.all()[0]
    return {
        "title_ru": pokemon.title,
        "pokemon_id": pokemon.id,
        "img_url": request.build_absolute_uri(pokemon.image.url)
    }
