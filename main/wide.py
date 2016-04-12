#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import traceback, linecache


def getException(printout=False):
	exc_type, exc_obj, tb = sys.exc_info()
	__frame = tb.tb_frame
	lineno = tb.tb_lineno
	filename = __frame.f_code.co_filename
	linecache.checkcache(filename)
	line = linecache.getline(filename, lineno, __frame.f_globals).strip()

	if printout:
		print '-'*50
		print '{0:>40}: {1}'.format( 'Exception in file {0}'.format(filename), lineno )
		print '{0:>40}: {1}'.format( 'line', line )
		print '{0:>40}: {1}'.format( 'type', exc_type )
		print '{0:>40}: {1}'.format( 'message', exc_obj )
		print 'full traceback:'
		traceback.print_exc()
		print '-'*50

	return 'file: {0}:{1}, type: {2}, error: {3}'.format(filename, lineno, exc_type, exc_obj)
