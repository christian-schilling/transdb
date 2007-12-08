from django.db import models
from django.conf import settings
from widgets import TransDbWidget

class TransDbField(models.Field):
	__metaclass__ = models.SubfieldBase

	def __init__(self, *args, **kwargs):
		num_lang = len(settings.LANGUAGES)
		kwargs['max_length'] = 2 + num_lang * 12 + kwargs['max_length'] * num_lang * 2
		super(TransDbField, self).__init__(*args, **kwargs)

	def get_internal_type(self):
		return 'CharField'

	def formfield(self, **kwargs):
		kwargs['widget'] = TransDbWidget
		return super(TransDbField, self).formfield(**kwargs)

	def to_python(self, value):
		if value:
			return eval(value)
	
	def get_db_prep_save(self, value):
		return str(value)

