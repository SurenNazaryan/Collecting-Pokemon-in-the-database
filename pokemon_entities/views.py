import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from .models import Pokemon, PokemonEntity
from django.utils import timezone


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
    current_time = timezone.localtime()
    pokemons_for_map = PokemonEntity.objects.filter(
        appeared_at__lt=current_time,
        disappeared_at__gt=current_time
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons_for_map:
        pokemon = pokemon_entity.pokemon
        image_url = (
            request.build_absolute_uri(pokemon.image.url)
            if pokemon.image.url
            else DEFAULT_IMAGE_URL
        )
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            image_url
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        image_url = (
            pokemon.image.url
            if pokemon.image
            else DEFAULT_IMAGE_URL
        )
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': image_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=int(pokemon_id))

    previous_evolution_data = None
    if requested_pokemon.previous_evolution:
        img_url = (
            requested_pokemon.previous_evolution.image.url
            if requested_pokemon.previous_evolution.image
            else DEFAULT_IMAGE_URL
        )
        previous_evolution_data = {
            "title_ru": requested_pokemon.previous_evolution.title,
            "pokemon_id": requested_pokemon.previous_evolution.id,
            "img_url": img_url
        }

    next_evolution_data = None
    if requested_pokemon.next_evolution.exists():
        next_evolution = requested_pokemon.next_evolution.first()
        img_url = (
            next_evolution.image.url
            if next_evolution.image
            else DEFAULT_IMAGE_URL
        )
        next_evolution_data = {
            "title_ru": next_evolution.title,
            "pokemon_id": next_evolution.id,
            "img_url": img_url
        }

    pokemon_data = {
        'pokemon_id': requested_pokemon.id,
        'img_url': (
            requested_pokemon.image.url
            if requested_pokemon.image
            else DEFAULT_IMAGE_URL
        ),
        'title_ru': requested_pokemon.title,
        'description': requested_pokemon.description,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'previous_evolution': previous_evolution_data,
        'next_evolution': next_evolution_data
    }

    current_time = timezone.localtime()
    pokemons_for_map = PokemonEntity.objects.filter(
        pokemon=requested_pokemon,
        appeared_at__lt=current_time,
        disappeared_at__gt=current_time
        )
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons_for_map:
        image_url = (
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
            if pokemon_entity.pokemon.image.url
            else DEFAULT_IMAGE_URL
        )
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            image_url
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_data
    })
