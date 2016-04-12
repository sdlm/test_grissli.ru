#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django import forms

# ---------------------------------------------------- Models

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


# ----------------------------------------------- helpers

def getRunLogPlainText():
	runLogRecords = TaskRunLog.objects.all()
	runLog_plain = ''
	for rec in runLogRecords:
		runLog_plain += '{} [{}] url: {}'.format(
				rec.timeStamp.strftime('%d.%m.%Y %H:%M:%S'), 
				'success' if rec.status == 0 else 'failure',
				rec.url
			)
		if rec.comment != None:
			runLog_plain += ' comment: {}\n'.format(rec.comment)
		else:
			runLog_plain += '\n'
	return runLog_plain

def getResultsLogPlainText():
	results = ResultLog.objects.all()
	results_plain = ''
	for r in results:
		results_plain += u'encoding: {}, title: "{}"'.format(
				r.encoding if r.encoding != None else 'undef',
				r.title
			)
		if r.h1 != None:
			results_plain += u', h1: "{}"\n'.format(r.h1)
		else:
			results_plain += '\n'
	return results_plain