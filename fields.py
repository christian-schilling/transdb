from django.db import models
from django.conf import settings
from django.utils.translation import get_language
from widgets import TransCharWidget, TransTextWidget
from django.db.models import signals
from django.dispatch import dispatcher

class TransDbValue:
	def __init__(self, value):
		try:
			self.value = eval(value)
		except:
			self.value = {}
		if not isinstance(self.value, dict):
			self.value = {}

	def __unicode__(self):
		if self.value.has_key(get_language()):
			return self.value[get_language()]
		elif self.value.has_key(settings.LANGUAGE_CODE):
			return self.value[settings.LANGUAGE_CODE]
		else:
			return ''
	
	def has_key(self, key):
		return self.value.has_key(key)

	def __getitem__(self, identifier):
		return self.value[identifier]

class TransField(models.Field):
	def to_python(self, value):
		if value:
			value_dict = eval(value)
			if isinstance(value_dict, dict):
				return value_dict
			else:
				return {}
		else:
			return {}
	
	def get_db_prep_save(self, value):
		value = unicode(value)
		return super(TransField, self).get_db_prep_save(value)

	#def post_init(self, instance=None):
		#value = getattr(instance, self.attname)
		#value = TransDbValue(value)
		#setattr(instance, self.attname, value)

	#def contribute_to_class(self, cls, name):
		#super(TransTextField, self).contribute_to_class(cls, name)
		#dispatcher.connect(self.post_init, signal=signals.post_init, sender=cls)

class TransTextField(TransField):
	__metaclass__ = models.SubfieldBase

	def get_internal_type(self):
		return 'TextField'

	def formfield(self, **kwargs):
		kwargs['widget'] = TransTextWidget
		return super(TransTextField, self).formfield(**kwargs)


class TransCharField(TransField):
	__metaclass__ = models.SubfieldBase

	def __init__(self, *args, **kwargs):
		num_lang = len(settings.LANGUAGES)
		kwargs['max_length'] = 2 + num_lang * 12 + kwargs['max_length'] * num_lang * 2
		super(TransCharField, self).__init__(*args, **kwargs)

	def get_internal_type(self):
		return 'CharField'

	def formfield(self, **kwargs):
		kwargs['widget'] = TransCharWidget
		return super(TransCharField, self).formfield(**kwargs)

