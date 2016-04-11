#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import time
from datetime import timedelta

# ---------------------------------------------------- Django
from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse, JsonResponse
# from django.conf import settings

from webparser.models import *
from webparser.tasks import *




from pprint import pprint
from datetime import datetime
import traceback, linecache
import socket

def printException(getErrorStack = False, file = None):
	exc_type, exc_obj, tb = sys.exc_info()
	__frame = tb.tb_frame
	lineno = tb.tb_lineno
	filename = __frame.f_code.co_filename
	linecache.checkcache(filename)
	line = linecache.getline(filename, lineno, __frame.f_globals).strip()

	if file == None:

		print '-'*50
		print '{0:>40}: {1}'.format( 'Exception in file {0}'.format(filename), lineno )
		print '{0:>40}: {1}'.format( 'line', line )
		print '{0:>40}: {1}'.format( 'type', exc_type )
		print '{0:>40}: {1}'.format( 'message', exc_obj )

		print 'full traceback:'
		traceback.print_exc()
		print '-'*50

	else:
		file.write('{0:>40}: {1}\n'.format( 'Exception in file {0}'.format(filename), lineno ))
		file.write('{0:>40}: {1}\n'.format( 'line', line ))
		file.write('{0:>40}: {1}\n'.format( 'type', exc_type ))
		file.write('{0:>40}: {1}\n'.format( 'message', exc_obj ))

		file.write('full traceback:\n')
		traceback.print_exc(file = file)

	if getErrorStack == False:
		return 'Exception in file {0} (line: {1}): {2}'.format(filename, line, exc_obj)

	else:
		temp = tempfile.TemporaryFile()
		rez = ''
		try:
			traceback.print_exc(file = temp)
			temp.seek(0)
			rez = temp.read()
		except Exception:
			print '-'*80
			print 'printException:: Exception rised near TemporaryFile'
			print '-'*80
		finally:
			temp.close()
		return rez



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
		results_plain += u'encoding: {}, title: "{}"'.format(
				r.encoding if r.encoding != None else 'undef',
				r.title
			)
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
		'url_form': TargetForm(),
	}
	context = RequestContext(request, content)
	return HttpResponse(template.render(context))


def admin(request):

	print 'api/admin executed !!'

	success = False

	try:
		action = request.POST['action']

		if action == 'addUrl':
			url = request.POST['url']

			shift = request.POST['shift']

			# todo optimize regex
			if re.match('^\d+$', shift)\
				or re.match('^(\d+):(\d\d)$', shift)\
				or re.match('^(\d+):$', shift)\
				or re.match('^:(\d\d)$', shift):

				if re.match('^\d+$', shift):
					sec = int(shift)

				elif re.match('^(\d+):(\d\d)$', shift):
					res = re.search('^(\d+):(\d\d)$', shift)
					sec = int(res.group(1))*60 + int(res.group(2))

				elif re.match('^(\d+):$', shift):
					res = re.search('^(\d+):$', shift)
					sec = int(res.group(1))*60

				elif re.match('^:(\d\d)$', shift):
					res = re.search('^:(\d\d)$', shift)
					sec = int(res.group(1))
			else:
				return JsonResponse( {'success': success}, safe = False )


			shift = timedelta(seconds = sec)
			worker(url, shift, addTarget = True)

		elif action == 'check':
			lastId = TaskRunLog.objects.values('id').order_by('-id')[0]
			return JsonResponse( {'success': success, 'id': lastId}, safe = False )

		success = True

	except Exception:
		printException()

	return JsonResponse( {'success': success}, safe = False )