from django.db import models
from datetime import date

from django.urls import reverse


class Category(models.Model):
    name = models.CharField("Категория", max_length=45)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=70, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Actor(models.Model):
    name = models.CharField("Актёр или режисёр", max_length=45)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="actors/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("actor_detail", kwargs={"slug": self.name})


    class Meta:
        verbose_name = "Актёр и режисёр"
        verbose_name_plural = "Актёры и режисёры"


class Genre(models.Model):
    name = models.CharField("Жанр", max_length=45)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=70, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Movie(models.Model):
    title = models.CharField("Фильм", max_length=45)
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Дата выхода", default=2020)
    director = models.ManyToManyField(Actor, verbose_name="Актёры", related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="Режисёры", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="Жанры")
    premiere = models.DateField("Премьера", default=date.today)
    budget = models.PositiveIntegerField("Бюджет", default=0, help_text="Сумма в доларах")
    fees = models.PositiveIntegerField("Сборы", default=0, help_text="Сумма в доларах")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=70, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})
    
    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class MovieShots(models.Model):
    title = models.CharField("Заголовок", max_length=45)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр"
        verbose_name_plural = "Кадры"


class RatingStar(models.Model):
    value = models.PositiveSmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезда рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    ip = models.CharField("Ip адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="звезда")

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField("Имя", max_length=35)
    text = models.TextField("Сообщение", max_length=550)
    parent = models.ForeignKey('self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, verbose_name="фильм", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"