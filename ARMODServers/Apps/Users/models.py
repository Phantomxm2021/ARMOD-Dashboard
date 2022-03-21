from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel

# Create your models here.
class User(AbstractUser, BaseModel):
    """User"""
    user_uid = models.BigIntegerField(default = -1,db_index=True,verbose_name='User Id')
    class Meta:
        db_table = 'armod_user'
        verbose_name = 'Users'
        verbose_name_plural = verbose_name
