#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# django_socketio
from django_socketio import broadcast_channel
from django_socketio.events import on_message

# my
from webparser.models import *
from main.wide import *
import tasks

def prepareData():
	return {
		'action': 'rerender_terminals',
		'runLog': tasks.getRunLogPlainText(),
		'resultsLog': tasks.getResultsLogPlainText(),
		'count': {'success': tasks.getSuccessCount(), 'failure': tasks.getFailCount()}
	}

def updateClientsData():
	print('updateClientsData()')
	try:
		broadcast_channel(prepareData(), channel='terminal')
		print('successfully send message !')
	except:
		getException(printout=True)


@on_message(channel="terminal")
def my_message_handler(request, socket, context, message):
	print('message_handler receive: {0}'.format(message))
	try:
		if message == 'update_request':
			socket.send(prepareData())
		if message == 'drop_results_request':
			tasks.dropResults()
	except:
		getException(printout=True)
