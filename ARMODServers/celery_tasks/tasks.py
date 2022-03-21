#!usr/bin/env python
# -*- coding:utf-8 -*-
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from celery import Celery
import time
import json

from django.db.models import Q

# django环境的初始化，在任务处理者worker一端加以下几句
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ARMODServers.settings')
django.setup()

# from Apps.goods.models import GoodsType, IndexGoodsBanner, IndexPromotionBanner, IndexTypeGoodsBanner

# 创建一个Celery类的实例对象
app = Celery('celery_tasks.tasks', broker='redis://localhost:6379/8')


# 定义任务函数
@app.task
def send_register_active_email(to_email, html_message):
    """发送激活邮件"""
    # 组织邮件信息
    subject = 'XRMOD'
    message = ''
    sender = settings.EMAIL_PROM  # 发送人
    receiver = [to_email]
    send_mail(subject, message, sender, receiver, html_message=html_message)


@app.task
def generate_static_index_html():
    """产生首页静态页面"""
    from Apps.Index.models import IndexPageViewKeyBenfitsModel,IndexPageQAModel,IndexSocialNavbar
    from Apps.Index.models import IndexNavbar,IndexHeader,IndexGuides,IndexPageViewMainKeyBenfitsModel,IndexGuideFeatures

    header = IndexHeader.objects.all().first()
    guide = IndexGuides.objects.all().first()
    keybenfits = IndexPageViewKeyBenfitsModel.objects.all().order_by('sort_id')
    main_keybenfits = IndexPageViewMainKeyBenfitsModel.objects.all().order_by('sort_id')
    qas = IndexPageQAModel.objects.all()
    navbars = IndexNavbar.objects.filter(Q(navbar_display=True),~Q(sort_id=99)).order_by('sort_id') 
    guide_features = IndexGuideFeatures.objects.all()
    social_navbars = IndexSocialNavbar.objects.all()
    # for feature in guide_features:
    #     print(type(feature.guide_feature_tags))
    #     jsondata = json.dumps(feature.guide_feature_tags)
    #     feature.guide_feature_tags = jsondata
    #     print(type(feature.guide_feature_tags))

    try:
        dashboard_nav = IndexNavbar.objects.get(navbar_display=True,sort_id=99)
    except IndexNavbar.DoesNotExist:
        dashboard_nav = None

    print(type(keybenfits[0].keybenfit_tags))
    context = {'main_keybenfits':main_keybenfits,'keybenfits': keybenfits,'qas':qas,'navbars':navbars,'header':header,
               'guide':guide,"dashboard_nav":dashboard_nav,"guide_features":guide_features,"social_navbars":social_navbars}
    static_index_html = render_to_string('index/index_test.html',context).encode('utf8')
    save_path = os.path.join(settings.BASE_DIR, 'templates/index/static_index.html')
    with open(save_path, 'wb') as f:
        f.write(static_index_html)