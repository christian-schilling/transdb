from django.db import models
from django.conf import settings
from django.utils.translation import get_language
from widgets import TransCharWidget, TransTextWidget
from django.core import validators
from django.utils.translation import ugettext as _

class TransDbValue(unicode):
	raw_data = {}

	def get_in_language(self, language):
		if self.raw_data and self.raw_data.has_key(language):
			return self.raw_data[language]
		else:
			return ''

class TransField(models.Field):
	def to_python(self, value):
		# TODO: Clean-up this method
		if value:
			try:
				value_dict = eval(value)
			except Exception:
				value_dict = value
			if isinstance(value_dict, dict):
				if value_dict[settings.LANGUAGE_CODE] or self.null:
					if value_dict[get_language()]:
						value = TransDbValue(value_dict[get_language()])
					else:
						value = TransDbValue(value_dict[settings.LANGUAGE_CODE])
					value.raw_data = value_dict
					return value
				else:
					raise validators.ValidationError, _("This field cannot be null.")
			else:
				value = TransDbValue(value)
				value.raw_data = {settings.LANGUAGE_CODE: value}
				return value
		elif self.null:
			value = TransDbValue('')
			value.raw_data = {}
			return value
		else:
			raise validators.ValidationError, _("This field cannot be null.")
	
	def get_db_prep_save(self, value):
		value = unicode(value.raw_data)
		return super(TransField, self).get_db_prep_save(value)

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
		kwargs['max_length'] = 2 + num_lang * 12 + kwargs['max_length'] * num_lang * 2 # Estimated maximum size for a dict with all translated strings
		super(TransCharField, self).__init__(*args, **kwargs)

	def get_internal_type(self):
		return 'CharField'

	def formfield(self, **kwargs):
		kwargs['widget'] = TransCharWidget
		return super(TransCharField, self).formfield(**kwargs)

