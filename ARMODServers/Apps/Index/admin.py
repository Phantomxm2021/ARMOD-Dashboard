from django.contrib import admin
from Apps.Index.models import IndexPageViewKeyBenfitsModel,IndexPageQAModel,IndexNavbar
from Apps.Index.models import IndexHeader,IndexGuides,IndexPageViewMainKeyBenfitsModel
from Apps.Index.models import IndexGuideFeatures,IndexSocialNavbar
# Register your models here.

class IndexPageViewKeyBenfitsAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request,obj,form,change)        
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()

    def delete_model(self, request, obj):
        super().delete_model(request,obj)
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()
        
admin.site.register(IndexPageViewKeyBenfitsModel,IndexPageViewKeyBenfitsAdmin)
admin.site.register(IndexPageQAModel,IndexPageViewKeyBenfitsAdmin)
admin.site.register(IndexNavbar,IndexPageViewKeyBenfitsAdmin)
admin.site.register(IndexHeader,IndexPageViewKeyBenfitsAdmin)
admin.site.register(IndexGuides,IndexPageViewKeyBenfitsAdmin)
admin.site.register(IndexPageViewMainKeyBenfitsModel,IndexPageViewKeyBenfitsAdmin)
admin.site.register(IndexGuideFeatures,IndexPageViewKeyBenfitsAdmin)
admin.site.register(IndexSocialNavbar,IndexPageViewKeyBenfitsAdmin)