# -*- coding: utf-8 -*-

from django.db import models

class TaskResult(models.Model):
    uuid = models.CharField(max_length=100, unique=True, db_index=True)
    result = models.TextField(blank=True, null=True, default=None)
