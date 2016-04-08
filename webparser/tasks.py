#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# system
import sys, os
import time
import requests
from bs4 import BeautifulSoup
import re
import linecache

# my
from webparser.models import *

def getException():
	exc_type, exc_obj, tb = sys.exc_info()
	__frame = tb.tb_frame
	lineno = tb.tb_lineno
	filename = __frame.f_code.co_filename
	linecache.checkcache(filename)
	line = linecache.getline(filename, lineno, __frame.f_globals).strip()

	return 'file: {0}:{1}, type: {2}, error: {3}'.format(filename, lineno, exc_type, exc_obj)

def has_charset(tag):
    return tag.has_attr('charset')

def worker(url, timeShift = None):

	try:
		time.sleep(timeShift.seconds)

		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
		r = requests.get(url, headers = headers)
		soup = BeautifulSoup(r.text)

		title = soup.find('title').text.strip()
		encoding = None
		encodingTag = soup.find('meta', {'http-equiv': 'content-type'})
		if encodingTag == None:
			encodingTag = soup.find('meta', {'http-equiv': 'Content-Type'})
		if encodingTag == None:
			charsets = soup.find_all(has_charset)
			encoding = charsets[0].get('charset')

		if encoding == None:
			encodingContent = encodingTag.get('content')
			encoding = re.search( r'^text\/html; charset=(.*)$', encodingContent).group(1)

		h1tag = soup.find('h1')
		if h1tag != None:
			h1 = h1tag.text.strip()

		record = TaskRunLog()
		record.url = url
		record.timeShift = timeShift if timeShift != 0 else None
		record.status = 0
		record.save()

		result = ResultLog()
		result.task = record
		result.encoding = encoding
		result.title = title
		result.h1 = h1 if h1tag != None else None
		result.save()

	except:
		record = TaskRunLog()
		record.url = url
		record.timeShift = timeShift
		record.status = 1
		record.comment = getException()
		# todo: wtite detailed error
		record.save()