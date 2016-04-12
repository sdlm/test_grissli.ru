#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django import forms


class Target(models.Model):
	url = models.CharField(max_length=1024)
	timeShift = models.DurationField(null=True, blank=True)

class TargetForm(forms.Form):
	url = forms.CharField(label='URL', max_length=1024)
	timeShift = forms.DurationField()

class TaskRunLog(models.Model):
	url = models.CharField(max_length=1024)
	timeShift = models.DurationField(null=True, blank=True)
	timeStamp = models.DateTimeField(auto_now=True)
	status = models.IntegerField()
	# 0 - success
	# 1 - failure
	# 2 - reserved
	comment = models.CharField(max_length=1024, null=True, blank=True)

class ResultLog(models.Model):
	task = models.ForeignKey(TaskRunLog)
	encoding = models.CharField(max_length=32, null=True, blank=True)
	title = models.CharField(max_length=1024, null=True, blank=True)
	h1 = models.CharField(max_length=1024, null=True, blank=True)


class UploadFileForm(forms.Form):
	file = forms.FileField(widget=forms.FileInput(attrs={'class': 'my-file-input'}))