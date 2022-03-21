from django.db import models
from db.base_model import BaseModel
from django.core.cache import cache
# Create your models here.
class ARExperienceModel(BaseModel):
    """应用信息"""
    arexperience_uid = models.BigIntegerField(null=True,blank=True,db_index=True,verbose_name='AR体验项目的ID')
    name = models.CharField(max_length = 64,unique=True,db_index=True,verbose_name='项目名称')
    app_uid = models.BigIntegerField(default = -1,db_index=True,verbose_name='所属应用的Id')
    # user_uid =  models.IntegerField(default = -1,db_index=True,verbose_name='User uid')
    status = models.IntegerField(default = 1,db_index=True,verbose_name='项目状态')
    description = models.CharField(default='',max_length = 128,verbose_name='项目描述')   
    class Meta:
        db_table = 'armod_arexperiences'
        verbose_name = 'ARExperiences'
        verbose_name_plural = verbose_name

  
class ARExperienceAsset(BaseModel):
    arexperience_uid =  models.BigIntegerField(null=True,db_index=True,verbose_name='所属项目的Id')
    android_json= models.CharField(max_length = 128,verbose_name='android json')   
    android_bundle= models.CharField(max_length = 128,verbose_name='android bundle')   
    android_bundle_size = models.FloatField(default = -1,verbose_name='android bundle size')
    ios_json= models.CharField(max_length = 128,verbose_name='ios json')   
    ios_bundle= models.CharField(max_length = 128,verbose_name='ios bundle')
    ios_bundle_size = models.FloatField(default = -1,verbose_name='ios bundle size')
    class Meta:
        db_table = 'armod_arexperience_assets'
        verbose_name = 'ARExperience Assets'
        verbose_name_plural = verbose_name

# Create your models here.
def getJSONFieldDefault():
    return []


class ARExperienceModelV2(BaseModel):
    """ARExperience"""
    app_uid = models.BigIntegerField(default = -1,db_index=True,verbose_name='所属应用的Id')
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
    project_id =  models.BigIntegerField(null=True,db_index=True,verbose_name='所属项目的Id')
    json_url= models.CharField(max_length = 128,verbose_name='android json')   
    bundle_url= models.CharField(max_length = 128,verbose_name='android bundle')   
    bundle_size = models.FloatField(default = -1,verbose_name='android bundle size')
    platform_type = models.CharField(max_length=16,verbose_name='Platform')
    class Meta:
        db_table = 'armod_arexperience_assets_v2'
        verbose_name = 'ARExperienceAssets_V2'
        verbose_name_plural = verbose_name




class Statistics(models.Model):
    pv = models.IntegerField(default=0,verbose_name="浏览次数")
    uv = models.IntegerField(default=0,verbose_name="浏览人数")
    date = models.CharField(max_length=200)
    project_id =  models.BigIntegerField(null=True,db_index=True,verbose_name='所属项目的Id')