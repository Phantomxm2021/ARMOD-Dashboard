from django.db import models
from db.base_model import BaseModel
from django.core.cache import cache

# Create your models here.
class TagsModel(BaseModel):
    user_uid = models.BigIntegerField(default=-1, db_index=True, verbose_name='User uid')
    app_uid = models.BigIntegerField(default=-1, db_index=True, verbose_name='App uid')
    tag_reference_weight = models.IntegerField(default=0,verbose_name='reference')
    tag_sort_weight = models.IntegerField(default=-1, verbose_name='Sort weight')
    tag_name = models.CharField(blank=True, max_length=16, db_index=True, verbose_name='Tag name')
    tag_key = models.CharField(default="", max_length=32, db_index=True,  verbose_name='Tag key')

    class Meta:
        db_table = 'armod_tags_v2'
        verbose_name = 'Tag_Manager_V2'
        verbose_name_plural = verbose_name 

    # def save(self, *args, **kwargs):       
    #     # cache.delete(f"api_{self.user_uid}_{self.app_uid}_{self.tag_name}_get_showcaseList")
    #     query_showcase_tags_key = f"api_{self.user_uid}_{self.app_uid}_get_taglist"
    #     cache.delete(query_showcase_tags_key)
    #     super(TagsModel, self).save(*args, **kwargs)