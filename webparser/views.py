#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from datetime import timedelta

# Django
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext, loader

# my
from webparser.models import *
from webparser.tasks import *
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
	}
	return render(request, 'webparser/index.html', content);


# ----------------------------------------------- AJAX API

def admin(request):
	success = False

	try:
		action = request.POST['action']

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

		if action == 'update':
			return JsonResponse( {'success': success}, safe = False )

		success = True

	except Exception:
		getException(printout=True)

	return JsonResponse( {'success': success}, safe = False )