# -*- coding: utf-8 -*-

from celery import Celery


app = Celery()
app.config_from_object('celery_app.celeryconfig')