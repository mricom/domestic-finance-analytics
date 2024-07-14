from django.db import models

class Shop(models.Model): 
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

    class Meta:
        verbose_name = "Shop"
        verbose_name_plural = "Shops"
        ordering = ['name']