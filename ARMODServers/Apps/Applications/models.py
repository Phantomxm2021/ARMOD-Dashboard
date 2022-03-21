from django.db import models
from db.base_model import BaseModel
from Apps.Users.models import User

# Create your models here.
class ApplicationsModel(BaseModel):
    """Application infomation"""
    app_uid =  models.BigIntegerField(default = -1,primary_key=True,db_index=True,verbose_name='App Id')
    user_uid = models.BigIntegerField(default = -1,db_index=True,verbose_name='User Id')
    name = models.CharField(max_length = 64,verbose_name='App Name')
    packageid = models.CharField(max_length = 64,db_index=True,verbose_name='Package Name')
    description = models.CharField(max_length = 128,default='',verbose_name='App Description')
    token = models.CharField(default='',max_length = 256,verbose_name='License Token')
    child_project = models.IntegerField(default = 0,verbose_name='Project Count')
    class Meta:
        db_table = 'armod_applications'
        verbose_name = 'Applications'
        verbose_name_plural = verbose_name

class ApplicationsModelV2(BaseModel):
    """应用信息"""
    app_uid =  models.BigIntegerField(default = -1,unique=True,db_index=True,verbose_name='App Id')
    user_uid = models.BigIntegerField(default = -1,db_index=True,verbose_name='User Id')
    name = models.CharField(max_length = 24,unique=True,verbose_name='App Name')
    packageid = models.CharField(max_length = 64,db_index=True,verbose_name='Package Name')
    description = models.CharField(max_length = 128,default='',verbose_name='App Description')
    token = models.CharField(default='',max_length = 256,verbose_name='License Token')
    app_icon_image = models.CharField(max_length = 128,default='',verbose_name='App icon')
    child_project = models.IntegerField(default = 0,verbose_name='Project Count')
    class Meta:
        db_table = 'armod_applications_v2'
        verbose_name = 'Applications_V2'
        verbose_name_plural = verbose_name