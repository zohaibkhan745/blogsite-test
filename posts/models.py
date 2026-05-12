from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ('tech',      'Technology'),
    ('life',      'Lifestyle'),
    ('edu',       'Education'),
    ('fashion',      'LifeStyle'),
    ('econ',      'Economy'),
    ('other',     'Other'),
]

class Post(models.Model):
    author   = models.ForeignKey(User, on_delete=models.CASCADE) #ForeignKey means each post belongs to one user, one user can have many posts and posts are deleted whenever the user is removed.
    title    = models.CharField(max_length=200)
    content  = models.TextField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)#Autodrop down, a tuple
    date     = models.DateField(auto_now_add=True) # Automatic creation date is inserted
    def __str__(self):
        return self.title
