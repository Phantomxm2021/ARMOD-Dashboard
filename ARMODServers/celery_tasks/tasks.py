#!usr/bin/env python
# -*- coding:utf-8 -*-
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from celery import Celery
import time

from django.db.models import Q

# Initialization of the django environment, add the following sentences on the worker side of the task processor
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ARMODServers.settings')
django.setup()

# Create an instance object of the Celery class
app = Celery('celery_tasks.tasks', broker='redis://localhost:6379/8')


# Define task function
@app.task
def send_register_active_email(to_email, html_message):
    """Send activation email"""
    # Organize mail information
    subject = 'YOUR_SUBJECT'
    message = ''
    sender = settings.EMAIL_PROM  # SENDER
    receiver = [to_email]
    send_mail(subject, message, sender, receiver, html_message=html_message)