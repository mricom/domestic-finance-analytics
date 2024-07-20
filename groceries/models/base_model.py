from django.db import models

class BaseModel(models.Model): 
    """
    Abstract base class for all models.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 
        abstract = True
        verbose_name = "Base Model"
        verbose_name_plural = "Base Models"