from django.db import models


class ToDo(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.BooleanField(default=False)
    timestamp = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.title