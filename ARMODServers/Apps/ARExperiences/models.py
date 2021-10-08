from django.db import models
from db.base_model import BaseModel
from django.core.cache import cache
# Create your models here.
class ARExperienceModel(BaseModel):
    """ARExperience model

    Args:
        BaseModel ([BaseModel]): Abstract model
    """
    arexperience_uid = models.BigIntegerField(default = -1,primary_key=True,db_index=True,verbose_name='AR Experience Id')
    name = models.CharField(max_length = 64,unique=True,db_index=True,verbose_name='AR Experience Name')
    app_uid = models.BigIntegerField(default = -1,db_index=True,verbose_name='App Id')
    status = models.IntegerField(default = 1,db_index=True,verbose_name='AR Experience Project Status')
    description = models.CharField(default='',max_length = 128,verbose_name='AR Experience Descriptor')   
    class Meta:
        db_table = 'armod_arexperiences'
        verbose_name = 'ARExperiences'
        verbose_name_plural = verbose_name

  
class ARExperienceAsset(BaseModel):
    """ARExperience Assets Model

    Args:
        BaseModel ([BaseModel]): Abstract model
    """
    arexperience_uid =  models.BigIntegerField(default = -1,db_index=True,verbose_name='AR Experience Id')
    android_json= models.CharField(max_length = 128,verbose_name='Android Json')   
    android_bundle= models.CharField(max_length = 128,verbose_name='Android Bundle')   
    android_bundle_size = models.FloatField(default = -1,verbose_name='Android Bundle Size')
    ios_json= models.CharField(max_length = 128,verbose_name='iOS Json')   
    ios_bundle= models.CharField(max_length = 128,verbose_name='iOS Bundle')
    ios_bundle_size = models.FloatField(default = -1,verbose_name='iOS Bundle Size')
    class Meta:
        db_table = 'armod_arexperience_assets'
        verbose_name = 'ARExperience Assets'
        verbose_name_plural = verbose_name
