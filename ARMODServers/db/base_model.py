from django.db import models

class BaseModel(models.Model):
    """Abstract Model"""
    create_time = models.DateTimeField(auto_now_add=True,null=True, verbose_name='Create Time')
    update_time = models.DateTimeField(auto_now=True, null=True,verbose_name='Update Time')
    is_delete = models.BooleanField(default=False, verbose_name='Delete Flag')

    class Meta:
        abstract = True
