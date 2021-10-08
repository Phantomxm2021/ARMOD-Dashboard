from django.contrib import admin
from Apps.ARShowcasesCenter.models import ARShowcasesCenterModel,ARShowcasesAndTagsLinkModel,ARShowcasesTagsModel
# Register your models here.

admin.site.register(ARShowcasesCenterModel)
admin.site.register(ARShowcasesAndTagsLinkModel)
admin.site.register(ARShowcasesTagsModel)