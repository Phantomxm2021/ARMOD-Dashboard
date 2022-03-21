from calendar import c
from pyexpat import model
from statistics import mode
from rest_framework import serializers
from Apps.ARExperiences.models import ARExperienceModelV2,ARExperienceResourceV2

class GetARExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ARExperienceModelV2
        fields = ['app_uid','user_uid','project_id','project_name','project_brief','project_icon']


class GetARExperienceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ARExperienceModelV2
        fields = ['app_uid','user_uid','project_id','project_name','project_description','project_icon','project_header','project_preview']


class GetRecommendARExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ARExperienceModelV2
        fields = ['app_uid','user_uid','project_id','project_name','project_brief','project_header']

class GetARResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ARExperienceResourceV2
        fields = ['json_url','bundle_url','bundle_size','platform_type']
        read_only_fields = ['json_url','bundle_url','bundle_size','platform_type']   