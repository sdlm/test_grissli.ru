#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# django_socketio
from django_socketio import broadcast_channel
from django_socketio.events import on_message

# my
from webparser.tasks import *
from webparser.models import *
from main.wide import *


def updateClientsData():
	print 'updateClientsData()'
	try:
		content = {
			'action': 'rerender_terminals',
			'runLog': getRunLogPlainText(),
			'resultsLog': getResultsLogPlainText(),
		}
		broadcast_channel(content, channel='terminal')
		print 'successfully send message !'
	except:
		getException(printout=True)


@on_message(channel="terminal")
def my_message_handler(request, socket, context, message):
	if message == 'update_request':
		content = {
			'action': 'rerender_terminals',
			'runLog': getRunLogPlainText(),
			'resultsLog': getResultsLogPlainText(),
		}
		socket.send(content)