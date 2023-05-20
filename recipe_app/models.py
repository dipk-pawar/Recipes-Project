from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    posted_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="recipe_user"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="images/", null=True)

    def __str__(self):
        return self.title
