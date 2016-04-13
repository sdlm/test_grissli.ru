#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from datetime import timedelta
from pprint import pprint

# Django
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext, loader

# my
from webparser.models import *
from webparser.kernel.tasks import *
from main.wide import *


def index(request):
	
	content = {
		'page': 'index',
		'runLog': getRunLogPlainText(),
		'resultsLog': getResultsLogPlainText(),
		'url_form': TargetForm(),
		# bugfix for django_socketio
		'STATIC_URL': '/static/',
		'MEDIA_URL': '/media/',
		'uploadFileForm': UploadFileForm(),
		'count': {'success': getSuccessCount(), 'failure': getFailCount()}
	}
	return render(request, 'webparser/index.html', content);


# ----------------------------------------------- AJAX API

def admin(request):
	print('admin()')

	success = False

	try:
		action = request.POST['action']

		print('admin: action: {0}'.format(action))

		if action == 'addUrl':
			url = request.POST['url']

			if len(url) == 0:
				return JsonResponse( {'success': success}, safe = False )
			# todo add url verification

			sec = 0
			if len(request.POST['shift']) > 0:
				record = request.POST['shift']

				# todo optimize regex
				if re.match('^\d+$', record)\
					or re.match('^(\d+):(\d\d)$', record)\
					or re.match('^(\d+):$', record)\
					or re.match('^:(\d\d)$', record):

					if re.match('^\d+$', record):
						sec = int(record)

					elif re.match('^(\d+):(\d\d)$', record):
						res = re.search('^(\d+):(\d\d)$', record)
						sec = int(res.group(1))*60 + int(res.group(2))

					elif re.match('^(\d+):$', record):
						res = re.search('^(\d+):$', record)
						sec = int(res.group(1))*60

					elif re.match('^:(\d\d)$', record):
						res = re.search('^:(\d\d)$', record)
						sec = int(res.group(1))
				else:
					return JsonResponse( {'success': success}, safe = False )

			shift = timedelta(seconds = sec)
			worker(url, shift, addTarget = True)

		elif action == 'update':
			return JsonResponse( {'success': success}, safe = False )

		elif action == 'add_urls_request':
			if len(request.POST['text']) > 0:
				text = request.POST['text']
				for l in text.split('\n'):
					if re.match('^(\d\d):(\d\d) (.*)$', l):
						res = re.search('^(\d\d):(\d\d) (.*)$', l)
						sec = int(res.group(1))*60 + int(res.group(2))
						url = res.group(3)

						# print 'sec: {:_>4}, url: {}'.format(sec, url)

						shift = timedelta(seconds = sec)
						worker(url, shift, addTarget = True)

					else:
						return JsonResponse( {'success': success}, safe = False )



		success = True

	except Exception:
		getException(printout=True)

	return JsonResponse( {'success': success}, safe = False )