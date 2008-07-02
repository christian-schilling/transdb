#! /usr/bin/python
'''
TransDb Django application

TransDb provides translated fields into the Django application modules
using TransCharField (for single line texts) and TransTextField (for
multiple line texts).

Simple usage:

    from django.db import models
    import transdb

    class MyModel(models.Model):
        single_language_field = models.CharField(max_length=32)
        multi_language_field = transdb.TransCharField(max_length=32)

Further information is available at project page:
    http://code.google.com/transdb
'''
from fields import TransCharField, TransTextField

