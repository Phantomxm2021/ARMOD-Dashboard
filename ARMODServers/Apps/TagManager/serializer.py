from rest_framework import serializers
from Apps.TagManager.models import TagsModel



class GetTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagsModel
        fields = ['tag_name','tag_sort_weight']