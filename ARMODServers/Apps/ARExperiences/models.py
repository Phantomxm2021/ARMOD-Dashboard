from django.db import models
from db.base_model import BaseModel
from django.core.cache import cache
# Create your models here.

def getJSONFieldDefault():
    return []

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





class ARExperienceModelV2(BaseModel):
    """ARExperience"""
    app_uid = models.BigIntegerField(default = -1,db_index=True,verbose_name='AR Experience Id')
    user_uid = models.BigIntegerField(default=-1, db_index=True, verbose_name='User uid')
    project_id = models.BigIntegerField(default=-1, db_index=True, unique=True, verbose_name='Showcase uid')
    project_name = models.CharField(max_length=16, default='',db_index=True, unique=True, verbose_name='Showcase name')
    project_brief = models.CharField( max_length=64, default='',  verbose_name='Showcase brief')
    project_status = models.IntegerField( default=0,db_index=True, verbose_name='Showcase status')
    project_permission = models.IntegerField(default=1,db_index=True ,verbose_name='Showcase permission')
    project_icon = models.CharField(max_length=512, default='', verbose_name='Showcase icon')
    project_header = models.CharField(max_length=512, default='', verbose_name='Showcase header')
    project_preview = models.CharField(max_length=1024, default='', verbose_name='Showcase previews(json)')
    project_description = models.CharField(max_length=1024, default='',blank=True, verbose_name='Showcase description')
    project_recommend =  models.BooleanField(default=False,db_index=True ,verbose_name='Showcase recommend')
    project_tags = models.JSONField(default=getJSONFieldDefault, verbose_name='Showcase not index tags')
    project_weight  = models.IntegerField( default=0,db_index=True, verbose_name='Showcase Weight')
    
    class Meta:
        db_table = 'armod_arexperiences_v2'
        verbose_name = 'ARExperiences_V2'
        verbose_name_plural = verbose_name    
        
        


class ARExperienceResourceV2(BaseModel):
    project_id =  models.BigIntegerField(null=True,db_index=True,verbose_name='AR Experience Id')
    json_url= models.CharField(max_length = 128,verbose_name='android json')   
    bundle_url= models.CharField(max_length = 128,verbose_name='android bundle')   
    bundle_size = models.FloatField(default = -1,verbose_name='android bundle size')
    platform_type = models.CharField(max_length=16,verbose_name='Platform')
    class Meta:
        db_table = 'armod_arexperience_assets_v2'
        verbose_name = 'ARExperienceAssets_V2'
        verbose_name_plural = verbose_name




class Statistics(models.Model):
    pv = models.IntegerField(default=0,verbose_name="UV")
    uv = models.IntegerField(default=0,verbose_name="PV")
    date = models.CharField(max_length=200)
    project_id =  models.BigIntegerField(null=True,db_index=True,verbose_name='AR Experience Id')