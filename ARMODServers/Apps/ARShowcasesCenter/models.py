from django.db import models
from db.base_model import BaseModel
from django.core.cache import cache
from django.db.models.signals import pre_delete,post_save 
from django.dispatch import receiver
# Create your models here.
def getJSONFieldDefault():
    return []

class ARShowcasesCenterModel(BaseModel):
    """Showcase"""
    app_uid = models.BigIntegerField(default=-1, db_index=True, verbose_name='App uid')
    user_uid = models.BigIntegerField(default=-1, db_index=True, verbose_name='User uid')
    arexperience_uid = models.BigIntegerField(default=-1, db_index=True, verbose_name='ARExperience uid')
    showcase_uid = models.BigIntegerField(default=-1, db_index=True, unique=True, verbose_name='Showcase uid')
    showcase_name = models.CharField(max_length=16, default='',db_index=True, unique=True, verbose_name='Showcase name')
    showcase_brief = models.CharField( max_length=64, default='',  verbose_name='Showcase brief')
    showcase_status = models.IntegerField( default=0,db_index=True, verbose_name='Showcase status')
    showcase_permission = models.IntegerField(default=1,db_index=True ,verbose_name='Showcase permission')
    showcase_icon = models.CharField(max_length=512, default='', verbose_name='Showcase icon')
    showcase_header = models.CharField(max_length=512, default='', verbose_name='Showcase header')
    showcase_preview = models.CharField(max_length=1024, default='', verbose_name='Showcase previews(json)')
    showcase_description = models.CharField(max_length=1024, default='', verbose_name='Showcase description')
    showcase_recommend =  models.BooleanField(default=False,db_index=True ,verbose_name='Showcase recommend')
    showcase_not_index_tags = models.JSONField(default=getJSONFieldDefault, verbose_name='Showcase not index tags')
    
    class Meta:
        db_table = 'armod_showcases_center'
        verbose_name = 'Showcases'
        verbose_name_plural = verbose_name       

    def save(self, *args, **kwargs):       
        cache.delete(f"api_{self.user_uid}_{self.app_uid}_{self.showcase_uid}_get_showcaseList")
        cache.delete(f"api_{self.user_uid}_{self.app_uid}_get_showcaseList")
        cache.delete(f"api_{self.user_uid}_{self.app_uid}_get_recommendList")

        tags_link = ARShowcasesAndTagsLinkModel.objects.filter(app_uid=self.app_uid,showcase_uid=self.showcase_uid)
        for tag in tags_link:
            cache.delete(f"api_{self.user_uid}_{self.app_uid}_{tag.tag_name}_get_showcaseList")

        query_showcase_detail_key = f"api_{self.user_uid}_{self.app_uid}_{self.showcase_uid}_get_detail"
        cache.delete(query_showcase_detail_key)

        super(ARShowcasesCenterModel, self).save(*args, **kwargs)        

class ARShowcasesAndTagsLinkModel(BaseModel):
    app_uid = models.BigIntegerField(
        default=-1, db_index=True, verbose_name='App uid')
    user_uid = models.BigIntegerField(
        default=-1, db_index=True, verbose_name='User uid')
    showcase_uid = models.BigIntegerField(
        default=-1, db_index=True, verbose_name='Showcases uid')
    tag_name = models.CharField(
        default='', max_length=16, db_index=True, verbose_name='Tag name')

    class Meta:
        db_table = 'armod_showcases_tags_link'
        verbose_name = 'Showcases tags link'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):       
        cache.delete(f"api_{self.user_uid}_{self.app_uid}_{self.tag_name}_get_showcaseList")
        super(ARShowcasesAndTagsLinkModel, self).save(*args, **kwargs)        

class ARShowcasesTagsModel(BaseModel):
    user_uid = models.BigIntegerField(default=-1, db_index=True, verbose_name='User uid')
    app_uid = models.BigIntegerField(default=-1, db_index=True, verbose_name='App uid')
    tag_reference_weight = models.IntegerField(default=0, db_index=True, verbose_name='reference')
    tag_sort_weight = models.IntegerField(default=-1, db_index=True, verbose_name='Sort weight')
    tag_name = models.CharField(default='', max_length=16, db_index=True, unique=True, verbose_name='Tag name')

    class Meta:
        db_table = 'armod_showcases_tags'
        verbose_name = 'Showcases tags'
        verbose_name_plural = verbose_name 

    def save(self, *args, **kwargs):       
        cache.delete(f"api_{self.user_uid}_{self.app_uid}_{self.tag_name}_get_showcaseList")
        query_showcase_tags_key = f"api_{self.user_uid}_{self.app_uid}_get_tags"
        cache.delete(query_showcase_tags_key)
        super(ARShowcasesTagsModel, self).save(*args, **kwargs)


@receiver(pre_delete)
def delete_repo(sender, instance, **kwargs):    
    if sender == ARShowcasesAndTagsLinkModel or  sender == ARShowcasesTagsModel:
        get_showcaselist_by_tag_cache_key = f"api_{instance.user_uid}_{instance.app_uid}_{instance.tag_name}_get_showcaseList"
        query_showcase_tags_key = f"api_{instance.user_uid}_{instance.app_uid}_get_tags"       
        cache.delete(query_showcase_tags_key)    
        cache.delete(get_showcaselist_by_tag_cache_key)
    elif sender == ARShowcasesCenterModel:                
        cache.delete(f"api_{instance.user_uid}_{instance.app_uid}_get_showcaseList")    
        cache.delete(f"api_{instance.user_uid}_{instance.app_uid}_1_1_get_showcaseList")
        cache.delete(f"api_{instance.user_uid}_{instance.app_uid}_1_get_showcaseList")
        cache.delete(f"api_{instance.user_uid}_{instance.app_uid}_get_recommendList")

@receiver(post_save)
def save_repo(sender, instance, **kwargs):    
    if sender == ARShowcasesAndTagsLinkModel or sender == ARShowcasesTagsModel:
        get_showcaselist_by_tag_cache_key = f"api_{instance.user_uid}_{instance.app_uid}_{instance.tag_name}_get_showcaseList"
        query_showcase_tags_key = f"api_{instance.user_uid}_{instance.app_uid}_get_tags"       
        cache.delete(query_showcase_tags_key)    
        cache.delete(get_showcaselist_by_tag_cache_key) 
      
    elif sender == ARShowcasesCenterModel:
        tags_link = ARShowcasesAndTagsLinkModel.objects.filter(app_uid=instance.app_uid,showcase_uid=instance.showcase_uid)        
        for tag in tags_link:
            cache.delete(f"api_{instance.user_uid}_{instance.app_uid}_{tag.tag_name}_get_showcaseList")            
        cache.delete(f"api_{instance.user_uid}_{instance.app_uid}_get_showcaseList")            
        cache.delete(f"api_{instance.user_uid}_{instance.app_uid}_1_get_showcaseList")
        cache.delete(f"api_{instance.user_uid}_{instance.app_uid}_1_1_get_showcaseList")        

