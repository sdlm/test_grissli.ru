#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# django
from django.contrib import admin
from django import forms

# my
from webparser.models import *
from webparser.kernel.tasks import worker


class TargetForm(forms.ModelForm):
	timeShift = forms.DurationField(required=False, label='TimeShift (hh:mm:ss)', initial='00:00:00')
	class Meta:
		model = Target
		fields = ['url', 'timeShift', ]


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
	list_display = ('url', 'timeShift',)
	form = TargetForm

	def save_model(self, request, obj, form, change):
		obj.url = obj.url.strip()
		worker(obj.url, obj.timeShift)
		obj.save()


@admin.register(TaskRunLog)
class TaskRunLogAdmin(admin.ModelAdmin):
	list_display = ('url','timeShift','timeStamp','status','comment',)
