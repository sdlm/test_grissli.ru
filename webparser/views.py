#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# ---------------------------------------------------- Django
from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse, JsonResponse
# from django.conf import settings



def index(request):

	template = loader.get_template('webparser/index.html')
	content = {
		'page': 'index',
	}
	context = RequestContext(request, content)
	return HttpResponse(template.render(context))
