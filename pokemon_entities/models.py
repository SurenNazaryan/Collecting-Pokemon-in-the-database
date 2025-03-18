from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Имя покемона')
    image = models.ImageField(
        upload_to='pokemons',
        null=True,
        blank=True,
        verbose_name='Картинка'
        )
    description = models.TextField(blank=True, verbose_name='Описание')
    title_en = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Имя на английском'
        )
    title_jp = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Имя на японском'
        )
    previous_evolution = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='next_evolution',
        verbose_name='Предыдущая эволюция'
        )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name='entities',
        verbose_name='Покемон'
        )
    lat = models.FloatField(null=True, blank=True, verbose_name='Широта')
    lon = models.FloatField(null=True, blank=True, verbose_name='Долгота')
    appeared_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Появление'
        )
    disappeared_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Исчезновение')
    level = models.PositiveIntegerField(null=True, blank=True, verbose_name='Уровень')
    health = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Здоровье'
        )
    strength = models.PositiveIntegerField(null=True, blank=True, verbose_name='Сила')
    defence = models.PositiveIntegerField(null=True, blank=True, verbose_name='Защита')
    stamina = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Выносливость'
        )

    def __str__(self):
        return self.pokemon.title
