#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import time

# ---------------------------------------------------- Django
from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse, JsonResponse
# from django.conf import settings

from webparser.models import *

def index(request):

	runLogRecords = TaskRunLog.objects.all()
	print 'runLogRecords len: {}'.format(len(runLogRecords))
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

	results = ResultLog.objects.all()
	print 'results len: {}'.format(len(results))
	results_plain = ''
	for r in results:
		results_plain += u'encoding: {}, title: "{}"'.format(r.encoding, r.title)
		if r.h1 != None:
			results_plain += u', h1: "{}"\n'.format(r.h1)
		else:
			results_plain += '\n'
	
	encoding = models.CharField(max_length=32)
	title = models.CharField(max_length=1024)
	h1 = models.CharField(max_length=1024)


	template = loader.get_template('webparser/index.html')
	content = {
		'page': 'index',
		'runLog': runLog_plain,
		'results': results_plain,
	}
	context = RequestContext(request, content)
	return HttpResponse(template.render(context))
