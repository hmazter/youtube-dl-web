# -*- coding: utf-8 -*-
import os

bind = '0.0.0.0:'+os.environ['PORT']
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" in %(D)sµs'
