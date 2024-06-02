from django.db import models

class Anime(models.Model):
    mal_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    synopsis = models.TextField()
    trailer_url = models.URLField(null=True, blank=True)
    duration = models.CharField(max_length=50)
    aired = models.CharField(max_length=100)
    season = models.CharField(max_length=50)
    image_url = models.URLField()
    rank = models.IntegerField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    scored_by = models.IntegerField(null=True, blank=True)
    popularity = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50)
    rating = models.CharField(max_length=50)
    source = models.CharField(max_length=50)
    character_id=models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.title

class Character(models.Model):
    mal_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    image_url = models.URLField()
    role = models.CharField(max_length=100)  # Ensure this field is included
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='characters')
    character_id=models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class AnimeImage(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()

    def __str__(self):
        return f"Image for {self.anime.title}"
    
from django.contrib.auth.models import User

class UserPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preferences')
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True, blank=True)
    liked = models.BooleanField(default=False)

    # Add any additional fields you need to store user preferences