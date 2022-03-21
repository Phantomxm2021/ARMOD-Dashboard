from email.policy import default
from django.db import models
from db.base_model import BaseModel

# Create your models here.


def getJSONFieldDefault():
    return {}

class IndexPageViewMainKeyBenfitsModel(BaseModel):
    """Main Key benfit"""
    sort_id = models.IntegerField(
        default=0, db_index=True, verbose_name="Key benfit sort id")
    keybenfit_title = models.CharField(
        max_length=64, default='', unique=True, verbose_name='Key benfit title')
    keybenfit_description = models.CharField(
        max_length=1024, default='', verbose_name='Key benfit description')
    keybenfit_icon = models.CharField(
        max_length=32, default='', blank=True, verbose_name='Key benfit icon')

    class Meta:
        db_table = 'armod_index_main_key_benfits'
        verbose_name = 'Index Main Keybenfits'
        verbose_name_plural = verbose_name

class IndexPageViewKeyBenfitsModel(BaseModel):
    """Key benfit"""
    sort_id = models.IntegerField(
        default=0, db_index=True, verbose_name="Key benfit sort id")
    keybenfit_title = models.CharField(
        max_length=64, default='', unique=True, verbose_name='Key benfit title')
    keybenfit_description = models.CharField(
        max_length=1024, default='', verbose_name='Key benfit description')
    keybenfit_preview_url = models.CharField(
        max_length=256, default='', blank=True, verbose_name='Key benfit preview url')

    keybenfit_tags =  models.JSONField(default=getJSONFieldDefault,blank=True, verbose_name='Key benfit tags')

    class Meta:
        db_table = 'armod_index_key_benfits'
        verbose_name = 'Index Keybenfits'
        verbose_name_plural = verbose_name

class IndexPageQAModel(BaseModel):
    """QA"""
    sort_id = models.IntegerField(
        default=0, db_index=True, verbose_name="QA sort id")
    qa_title = models.CharField(
        max_length=64, default='', unique=True, verbose_name='QA title')
    qa_description = models.CharField(
        max_length=1024, default='', verbose_name='QA description')
    qa_extra = models.JSONField(default=getJSONFieldDefault, verbose_name='QA extra')
    class Meta:
        db_table = 'armod_index_qa'
        verbose_name = 'qas'
        verbose_name_plural = verbose_name

class IndexNavbar(BaseModel):
    """Navbar"""
    sort_id = models.IntegerField(
        default=0, db_index=True, verbose_name="Navbar sort id")
    navbar_title = models.CharField(
        max_length=16, default='', verbose_name='Navbar title')
    navbar_url = models.CharField(
        max_length=256, default='', blank=True, verbose_name='Navbar url')
    navbar_icon = models.CharField(
        max_length=32, default='', blank=True, verbose_name='Navbar icon')
    navbar_subs = models.JSONField(
        default=getJSONFieldDefault, blank=True, verbose_name='Navbar subs')
    navbar_display = models.BooleanField(
        default=True, verbose_name='Navbar status')

    class Meta:
        db_table = 'armod_index_navbar_test'
        verbose_name = 'navbar'
        verbose_name_plural = verbose_name

class IndexHeader(BaseModel):
    """Header"""
    header_name = models.CharField(
        max_length=64, default='', verbose_name='Header name')
    header_brief = models.CharField(
        max_length=128, default='', verbose_name='Header brief name')
    header_descript = models.CharField(
        max_length=512, default='', verbose_name='Header descript name')
    header_download_title = models.CharField(
        max_length=16, default='', blank=True, verbose_name='Header download title')
    header_download_url = models.CharField(
        max_length=256, default='', blank=True, verbose_name='Header download url')
    class Meta:
        db_table = 'armod_index_header'
        verbose_name = 'header'
        verbose_name_plural = verbose_name

class IndexGuides(BaseModel):
    """Guid"""
    guide_selection = models.CharField(
        max_length=16, default='', verbose_name='guide name')
    guid_description = models.CharField(
        max_length=512, default='', verbose_name='guide description')
    # guide_type = models.IntegerField(default=0, verbose_name="guide type")
    # guide_subs = models.JSONField(
    #     default=getJSONFieldDefault, verbose_name="guide subs")
    # guide_display = models.BooleanField(
    #     default=True, verbose_name='guide status')

    class Meta:
        db_table = 'armod_index_guides'
        verbose_name = 'Index Guides'
        verbose_name_plural = verbose_name

class IndexGuideFeatures(BaseModel):
    guide_feature_color = models.CharField(
        max_length=32, default='', verbose_name='guide feature color')

    guide_feature_icon = models.CharField(
        max_length=16, default='', verbose_name='guide feature icon')

    guide_feature_name = models.CharField(
        max_length=32, default='', verbose_name='guide feature name')
    
    guide_feature_description = models.CharField(
        max_length=512, default='', verbose_name='guide feature description')
    
    guide_feature_tags = models.JSONField(default=getJSONFieldDefault, verbose_name='guide feature tags')
    
class IndexSocialNavbar(BaseModel):
    social_navbar_title = models.CharField(
        max_length=16, default='', verbose_name='Social navbar title')
    social_navbar_url = models.CharField(
        max_length=256, default='', blank=True, verbose_name='Social navbar url')
    social_navbar_icon = models.CharField(
        max_length=32, default='', blank=True, verbose_name='Social navbar icon')
    social_navbar_subs = models.JSONField(
        default=getJSONFieldDefault, blank=True, verbose_name='Social navbar subs')
    social_navbar_display = models.BooleanField(
        default=True, verbose_name='Navbar status')

    class Meta:
        db_table = 'armod_index_social_navbar'
        verbose_name = 'social_navbar'
        verbose_name_plural = verbose_name