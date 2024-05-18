from django.db import models
from django.contrib.auth.models import User

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13)
    general = models.IntegerField()
    plot = models.IntegerField()
    characters = models.IntegerField()
    style = models.IntegerField()
    add_date = models.DateField(auto_now_add=True)
    review = models.TextField(null=True)

    def __str__(self):
        return f"{self.user.username} - {self.isbn} - {self.general} - {self.plot} - {self.characters} - {self.style}"

class Status(models.Model):
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.status

class User2Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    google_id = models.CharField(max_length=13)  # ISBN книги
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.google_id} - {self.status}"