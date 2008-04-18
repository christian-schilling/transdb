from django.db import models
from django.conf import settings
from django.utils.translation import get_language
from django.utils.translation import ugettext as _
from django.newforms.fields import Field
from django.newforms import ValidationError
from widgets import TransCharWidget, TransTextWidget

def get_default_language_name():
	'''
	Get language from default language specified by LANGUAGE_CODE in settings
	Used in error messages
	'''
	lang_name = ''
	for lang in settings.LANGUAGES:
		if lang[0] == settings.LANGUAGE_CODE:
			lang_name = lang[1]
			break
	return lang_name

class TransDbValue(unicode):
	'''
	This class implements a unicode string, but with a hidden attribute raw_data.
	When used as a string it returns the translation of the current language
	raw_data attribute stores a dictionary with all translations
	Also implements a method "get_in_language(language)" that returns the translation on any available language
	'''
	raw_data = {}

	def get_in_language(self, language):
		if self.raw_data and self.raw_data.has_key(language):
			return self.raw_data[language]
		else:
			return ''

class TransFormField(Field):
	'''
	newforms field, used when ModelForm (or deprecated form_for_model/form_form_instance) is called
	Also implements form validation in admin
	'''
	def clean(self, value):
		if self.required and not value[settings.LANGUAGE_CODE]:
			raise ValidationError, _("This field cannot be null for default language '%s'." % get_default_language_name())
		else:
			return value

class TransField(models.Field):
	'''
	Model field to be subclassed
	Used for storing a string in many languages at database (with python's dictionary format)
	pickle module could be used, but wouldn't alow search on fields?
	'''
	def get_manipulator_field_objs(self):
		return [FormTransField]

	def get_internal_type(self):
		return 'TextField'

	def to_python(self, value):
		if isinstance(value, dict): # formfield method makes this function be called with value as a dict
			python_value = value
		else:
			try:
				python_value = eval(value)
			except Exception:
				python_value = None
		if isinstance(python_value, dict) and python_value.has_key(settings.LANGUAGE_CODE):
			if python_value.has_key(get_language()) and python_value[get_language()]:
				result = TransDbValue(python_value[get_language()])
			else:
				result = TransDbValue(python_value[settings.LANGUAGE_CODE])
			result.raw_data = python_value
		else:
			result = TransDbValue(value)
			result.raw_data = {settings.LANGUAGE_CODE: value}
		return result
	
	def get_db_prep_save(self, value):
		return unicode(value.raw_data)

	def formfield(self, **kwargs):
		defaults = {'form_class': TransFormField}
		defaults.update(kwargs)
		return super(TransField, self).formfield(**defaults)

class TransCharField(TransField):
	'''
	TransField used with CharField widget
	'''
	__metaclass__ = models.SubfieldBase

	def formfield(self, **kwargs):
		kwargs['widget'] = TransCharWidget
		return super(TransCharField, self).formfield(**kwargs)

class TransTextField(TransField):
	'''
	TransField used with CharField widget
	'''
	__metaclass__ = models.SubfieldBase

	def formfield(self, **kwargs):
		kwargs['widget'] = TransTextWidget
		return super(TransTextField, self).formfield(**kwargs)

