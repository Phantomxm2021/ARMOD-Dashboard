from django.db import models
from db.base_model import BaseModel
from Apps.Users.models import User

# Create your models here.
class ApplicationsModel(BaseModel):
    """应用信息"""
    app_uid =  models.BigIntegerField(default = -1,primary_key=True,db_index=True,verbose_name='应用Id')
    user_uid = models.BigIntegerField(default = -1,db_index=True,verbose_name='用户Id')
    name = models.CharField(max_length = 64,verbose_name='应用名称')
    packageid = models.CharField(max_length = 64,db_index=True,verbose_name='应用绑定的包名')
    description = models.CharField(max_length = 128,default='',verbose_name='应用绑定的包名')
    token = models.CharField(default='',max_length = 256,verbose_name='应用用Token')
    child_project = models.IntegerField(default = 0,verbose_name='应用下项目数')
    class Meta:
        db_table = 'armod_applications'
        verbose_name = 'Applications'
        verbose_name_plural = verbose_name

class ApplicationsModelV2(BaseModel):
    """应用信息"""
    app_uid =  models.BigIntegerField(default = -1,unique=True,db_index=True,verbose_name='应用Id')
    user_uid = models.BigIntegerField(default = -1,db_index=True,verbose_name='用户Id')
    name = models.CharField(max_length = 24,unique=True,verbose_name='应用名称')
    packageid = models.CharField(max_length = 64,db_index=True,verbose_name='应用绑定的包名')
    description = models.CharField(max_length = 128,default='',verbose_name='应用绑定的包名')
    token = models.CharField(default='',max_length = 256,verbose_name='应用用Token')
    app_icon_image = models.CharField(max_length = 128,default='',verbose_name='应用绑定的包名')
    child_project = models.IntegerField(default = 0,verbose_name='应用下项目数')
    class Meta:
        db_table = 'armod_applications_v2'
        verbose_name = 'Applications_V2'
        verbose_name_plural = verbose_name