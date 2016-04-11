#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# system
import sys, os
import time
from datetime import timedelta
import re
import linecache

# webparsing
import requests
from bs4 import BeautifulSoup

# threading
import thread
from Queue import Queue
from threading import Thread

# my
from webparser.models import *

# Django
from django.conf import settings

# ----------------------------------------------- helpers
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




class Manager(object):
	"""Класс для манипуляции пула потоков при парсинге большого кол-ва страниц."""

	def __init__(self, num_threads = None):
		self.__num_threads = num_threads if num_threads != None else 10
		self.__q = Queue(maxsize=0)

		for i in xrange(self.__num_threads):
			worker = Thread(target=self.__do_stuff)
			worker.setDaemon(True)
			worker.start()

	def __do_stuff(self):
		while True:
			# print self.__q.get()
			url, timeShift = self.__q.get()
			print 'Manager.__do_stuff(): {}'.format(url)

			try:
				encoding, title, h1 = webParser(url, timeShift)

				record = TaskRunLog()
				record.url = url
				record.timeShift = timeShift if timeShift != 0 else None
				record.status = 0
				record.save()

				result = ResultLog()
				result.task = record
				result.encoding = encoding
				result.title = title
				result.h1 = h1
				result.save()
			except:
				pass

			self.__q.task_done()

	def addUrl(self, url, timeShift = None):
		time.sleep(timeShift.seconds)
		self.__q.put((url, timeShift))




def worker(url, timeShift = None, addTarget = False):

	# verification
	assert(type(url) == str or type(url) == unicode)
	if timeShift != None:
		assert(type(timeShift) == timedelta)

	if addTarget:
		target = Target()
		target.url = url
		target.timeShift = timeShift
		target.save()

	thread.start_new_thread( __inner_worker, (url, timeShift) )
	# webParser(url)


mm = Manager(settings.THREADS_COUNT)

def __inner_worker(url, timeShift = None):
	time.sleep(timeShift.seconds)
	mm.addUrl(url, timeShift)


	
def webParser(url, timeShift):
	try:
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
		if not (re.match('^http://', url) or re.match('^https://', url)):
			url = 'http://' + url
		r = requests.get(url, headers = headers)
		soup = BeautifulSoup(r.text)

		title = soup.find('title').text.strip()
		encoding = None
		encodingTag = soup.find('meta', {'http-equiv': 'content-type'})
		if encodingTag == None:
			encodingTag = soup.find('meta', {'http-equiv': 'Content-Type'})
		if encodingTag == None:
			charsets = soup.find_all(has_charset)
			if len(charsets) > 0:
				encoding = charsets[0].get('charset')

		if encoding == None and encodingTag != None:
			encodingContent = encodingTag.get('content')
			encoding = re.search( r'^text\/html; charset=(.*)$', encodingContent).group(1)

		h1tag = soup.find('h1')
		h1 = None
		if h1tag != None:
			h1 = h1tag.text.strip()
	except:
		record = TaskRunLog()
		record.url = url
		record.timeShift = timeShift
		record.status = 1
		record.comment = getException()
		record.save()

		raise Exception('error on parsing')

	return (encoding, title, h1)