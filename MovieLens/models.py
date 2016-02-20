from django.db import models


# Create your models here.

class Movie(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=30)
    genres = models.CharField(max_length=50)

    def __str__(self):
        info = 'id: ' + str(self.movie_id) + '\n' + \
               'title: ' + self.title + '\n' + \
               'genres: ' + self.genres + '\n'
        return info


class Rating(models.Model):
    user_id = models.IntegerField()
    movie = models.ForeignKey(Movie)
    movie_rating = models.FloatField()
    timestamp = models.IntegerField()

    def __str__(self):
        info = 'user_id: ' + str(self.user_id) + '\n' + \
               'movie_id: ' + str(self.movie) + '\n' + \
               'movie_rating: ' + str(self.movie_rating) + '\n' + \
               'timestamp: ' + str(self.timestamp) + '\n'
        return info


class Tag(models.Model):
    user_id = models.IntegerField()
    movie = models.ForeignKey(Movie)
    movie_tag = models.CharField(max_length=50)
    timestamp = models.IntegerField()

    def __str__(self):
        info = 'user_id: ' + str(self.user_id) + '\n' + \
               'movie_id: ' + str(self.movie) + '\n' + \
               'movie_tag: ' + str(self.movie_tag) + '\n' + \
               'timestamp: ' + str(self.timestamp) + '\n'
        return info
