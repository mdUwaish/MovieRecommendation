from django.db import models
from user_management.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, F, Count, FloatField


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children')

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    biography = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    release_date = models.DateField(auto_now=True)
    rating = models.FloatField(default=0.0)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    poster_image = models.ImageField(upload_to='images/', null=True, blank=True)
    genres = models.ManyToManyField(Genre, related_name='movies')
    actors = models.ManyToManyField(Actor, related_name='movies')

    def calculate_weighted_rating(self):
        reviews = self.reviews.all().select_related('user')
        if reviews.exists():
            weighted_ratings = reviews.annotate(
                user_review_count=Count('user__review_set')
            ).aggregate(
                weighted_rating=Avg(F('rating') * F('user_review_count'), output_field=FloatField()) / Avg(F('user_review_count'), output_field=FloatField())
            )
            self.rating = weighted_ratings['weighted_rating'] or 0.0
            self.save()


    def __str__(self):
        return self.title


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_set')
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(10)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('movie', 'user')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.movie.calculate_weighted_rating()

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} - {self.rating}"
    